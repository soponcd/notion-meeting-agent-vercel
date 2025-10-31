# 🧠 Notion Meeting Agent Hotfix v1.3.1

## 修复说明
- 兼容 `start` / `start_time` 与 `end` / `end_time` 字段。
- 统一响应格式。
- 可直接部署于 Vercel。

## 调用示例
POST https://notion-meeting-agent-vercel.vercel.app/meetings.create
Authorization: Bearer NINEHUI-7f3a-2025
Content-Type: application/json

{
  "title": "东汽焊接工装改进会议",
  "date": "2025-10-31",
  "start": "14:00",
  "end": "15:30",
  "attendees": "张伟, 李婷, 王强",
  "meeting_type": "沟通会",
  "discussion": "讨论焊接工装第二版的设计优化及成本控制方案。",
  "conclusion": "确认焊接工装第二版优化方案并启动供应商比价流程。",
  "todo": "准备供应商比价会议材料；完成二期设计图纸评审。",
  "status": "草稿"
}
