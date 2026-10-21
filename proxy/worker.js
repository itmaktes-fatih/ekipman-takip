// Cloudflare Worker: etiket fotoğrafını Google Gemini'ye okutur (ücretsiz katman).
// Ayarlar (Workers > Settings > Variables and Secrets, "Secret" olarak):
//   GEMINI_API_KEY  -> Google AI Studio'dan alınan API anahtarı
//   APP_TOKEN       -> uygulamadaki ETIKET_API_TOKEN ile aynı rastgele metin
//   MODEL (opsiyonel) -> varsayılan: gemini-2.5-flash

const SYSTEM = `Sen bir ekipman etiketi okuyucususun. Görsel, "ELEKTRİKLİ SEYYAR EKİPMAN İZOLASYON TEST KARTI" etiketidir (fotoğraf yan dönmüş olabilir).
Alanlar: "Ekipman Adı", "Ekipman Seri No", "Son Kontrol Tarihi". Son kontrol alanı basılı "/10-11-12/20..." biçimindedir; yıl elle yazılır.
Yalnızca şu JSON'u döndür, başka hiçbir şey yazma:
{"ekipman_adi": string|null, "seri_no": string|null, "aylar": [int], "yil": int|null, "notlar": string}
Kurallar:
- seri_no: harf/rakamları görüldüğü gibi yaz, tahmin yürütme. Karışan karakterler (S/5, L/2, O/0 gibi) varsa notlar'a yaz.
- aylar: son kontrol alanında BASILI olan ay numaraları (ör. /10-11-12/ -> [10,11,12]).
- yil: elle yazılan yılı 4 haneli yaz (26 -> 2026).
- Okunamayan alan null olsun. Emin olmadığın bir şey varsa notlar'da kısaca belirt (Türkçe).`;

export default {
  async fetch(request, env) {
    if (request.method !== "POST") return new Response("Yalnızca POST", { status: 405 });
    if (request.headers.get("X-App-Token") !== env.APP_TOKEN) {
      return new Response("Yetkisiz", { status: 401 });
    }

    let body;
    try { body = await request.json(); } catch { return new Response("Geçersiz JSON", { status: 400 }); }

    const { image_base64, mime } = body;
    if (!image_base64 || image_base64.length > 8_000_000) {
      return new Response("Görsel yok veya çok büyük", { status: 400 });
    }

    const model = env.MODEL || "gemini-2.5-flash";
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`;

    const r = await fetch(url, {
      method: "POST",
      headers: {
        "x-goog-api-key": env.GEMINI_API_KEY,
        "content-type": "application/json",
      },
      body: JSON.stringify({
        systemInstruction: { parts: [{ text: SYSTEM }] },
        contents: [{
          role: "user",
          parts: [
            { inline_data: { mime_type: mime || "image/jpeg", data: image_base64 } },
            { text: "Etiketi oku." },
          ],
        }],
        generationConfig: {
          temperature: 0,
          maxOutputTokens: 2000,
          responseMimeType: "application/json",
        },
      }),
    });

    if (r.status === 429) return new Response("Ücretsiz günlük/dakikalık sınır doldu", { status: 429 });
    if (!r.ok) return new Response("Okuma servisi hatası (" + r.status + ")", { status: 502 });

    const j = await r.json();
    const text = ((j.candidates || [])[0]?.content?.parts || [])
      .map(p => p.text || "").join("")
      .replace(/```json|```/g, "").trim();

    try {
      return new Response(JSON.stringify(JSON.parse(text)), {
        headers: { "content-type": "application/json" },
      });
    } catch {
      return new Response("Yanıt çözümlenemedi", { status: 502 });
    }
  },
};

