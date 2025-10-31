export default function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }
  res.status(200).json({
    success: true,
    data: [
      { id: "MTG-001", title: "测试会议", date: "2025-11-01" },
      { id: "MTG-002", title: "云端正式版验证会议", date: "2025-11-02" }
    ]
  });
}
