# Notion Meeting Agent — Vercel 部署版（HTTPS + API Key）

## 一、准备
1. 将本目录作为一个 Git 仓库上传到 GitHub（或直接导入到 Vercel）。
2. 打开 https://vercel.com ，Import 本仓库为一个新项目。

## 二、环境变量（Vercel → Project → Settings → Environment Variables）
- NOTION_TOKEN = 你的 Notion Integration Token（secret_... 或 ntn_...）
- DATABASE_ID  = 29dd6934-6604-813e-9960-fbad9839145a
- API_KEY      = 自定义一段随机字符串（例如：NINEHUI-<随机>）

保存后点击 **Deploy**。部署完成，得到一个 HTTPS URL，例如：
https://notion-meeting-agent.vercel.app

## 三、接口说明
- GET  /           健康检查
- POST /meetings.create  新增会议纪要
- POST /meetings.query   查询会议纪要

请求需携带：
Authorization: Bearer <API_KEY>
Content-Type: application/json

### 示例（创建会议）
curl -X POST "https://YOUR_VERCEL_URL/meetings.create" \
  -H "Authorization: Bearer YOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "title":"云端部署测试",
    "date":"2025-11-04",
    "start":"16:00",
    "end":"16:30",
    "attendees":["周光洪","何芬"],
    "meeting_type":"沟通会",
    "content":"云端Webhook写入验证",
    "decisions":"通过",
    "todos":"检查数据库同步",
    "status":"草稿"
  }'

## 四、ChatGPT Actions 集成
1. 打开 https://chat.openai.com/gpts/editor → 创建 GPT → Configure → Add Actions。
2. 将本仓库中的 `openapi.yaml` 内容复制粘贴到架构编辑器。
3. 将 `servers.url` 修改为你的 Vercel HTTPS 地址。
4. 在 “Authentication / 身份验证” 选择 **Bearer**，并填入你的 `API_KEY`。
5. 保存后测试 Action：让 GPT 发起创建会议请求。

## 五、常见问题
- 403/401：检查 Authorization 头是否为 `Bearer <API_KEY>`；检查 Vercel 环境变量已生效。
- 400 validation_error：检查 Notion 数据库属性字段是否与脚本中的中文名一致。
- 权限问题：确保 Notion 集成被添加到数据库父页面（Add connections to this page）。
