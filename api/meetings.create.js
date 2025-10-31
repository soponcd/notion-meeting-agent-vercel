export default function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const body = req.body;
  if (!body.title || !body.date || !body.start || !body.end) {
    return res.status(400).json({ error: "Missing required fields: title, date, start, end" });
  }

  // 模拟成功返回
  res.status(200).json({
    id: `MTG-${Date.now()}`,
    success: true,
    title: body.title,
  });
}
