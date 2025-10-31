export default function handler(req, res) {
  res.status(200).json({
    status: "ok",
    service: "Notion Meeting Agent",
    version: "1.4.3",
    timestamp: new Date().toISOString()
  });
}
