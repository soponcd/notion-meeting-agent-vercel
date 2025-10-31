export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }
  const { title, date, start, end } = req.body;
  if (!title || !date || !start || !end) {
    return res.status(400).json({ error: "Missing required fields: title, date, start, end" });
  }
  res.status(200).json({
    id: `MTG-${Date.now()}`,
    success: true,
    title,
  });
}
