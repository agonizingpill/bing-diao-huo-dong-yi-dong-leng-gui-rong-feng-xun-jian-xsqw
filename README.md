# 冰雕活动移动冷柜融缝巡检

河湾冰雕节搭建组留存成品接缝和柜格变化，从同格历史筛出稀少样并交给换格组签认。

## 现场工作与联系人

模拟客户为河湾冰雕节灯景搭建组。冰雕块码、空载测试、带载分区密度、冷区互换；旧冰模脱模区不得占用预留的成品转运位。

- 冰雕柜格档位 `cold_cells`，字段为 `duty`（功能区）、`authorized`（点位已授权）、`free_slots`（余位）、`closed`（停止使用）。模型约束位于 `backend/domain/cold_cells_model.py`，规则位于 `cold_cells_service.py`。
- 空载与冰雕实测 `thaw_samples`，字段为 `cell`（柜格）、`mass_kg`（冰灯质量 kg）、`melt`（接缝偏移 mm）、`drift`（相邻窗温漂）、`empty_test`（空载测试）、`piece`（冰雕码）。模型约束位于 `backend/domain/thaw_samples_model.py`，规则位于 `thaw_samples_service.py`。
- 融缝稠密程度 `seam_maps`，字段为 `sample`（冰雕实测）、`density`（局部相对密度）、`threshold`（基线门槛）、`decision`（人工复核指向）、`token`（计算凭据）。模型约束位于 `backend/domain/seam_maps_model.py`，规则位于 `seam_maps_service.py`。
- 冰雕跨格互换单 `cell_swaps`，字段为 `seam`（融缝复核）、`target`（目标柜格）、`handover`（现场双签）、`state`（状态）。模型约束位于 `backend/domain/cell_swaps_model.py`，规则位于 `cell_swaps_service.py`。

团队为模拟的10 人冰雕节搭建组，管理流动冷柜内的待布景单位。

搬移工从散页温度簿找接缝问题。空载试验容易掺进带载参考，脱模格和成品位有人误用，换格后空位常记在错误柜格。

带载接缝观测进入同柜格比较，两位搬移人确认格签，组长据此更新可用位。

### 一天的业务操作

1. 08:20 核对旧模脱模格 CELL-M。
2. 09:30 在 CELL-A 录入 24.2 kg 的 LAMP-11。
3. 10:00 从 30 条带载历史中取 22 条作近邻参考。
4. 11:00 签认 DENS-24 建议换格。
5. 13:30 拒绝换往脱模区，转入 CELL-B。
6. 14:30 江峰与罗岚回填格签，原格余位增至三。

## 启动

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec -T backend python -m scripts.seed_demo
```

打开 `http://127.0.0.1:18323`。FastAPI OpenAPI 在 `http://127.0.0.1:19323/docs`。
Compose 运行 Nginx、Python FastAPI、独立 Redis 消费进程、SQL 数据库和 Redis，SQL 与 Redis 使用命名卷。
本机开发时，在 Python 3.11 环境安装 `backend/requirements.txt` 后从 backend 目录运行 `uvicorn core.app:app`。须提供 `DATABASE_URL`、`REDIS_URL`、`JWT_SECRET`，`SEED_DEMO` 控制演示初始化。

| 演示账号 | 权限 |
|---|---|
| operator@demo.test | 提交领域记录和计算请求 |
| reviewer@demo.test | 提交记录并执行有业务约束的复核操作 |
| viewer@demo.test | 浏览业务台账 |

三个本地演示账号均使用 `DemoC0de!2026`。角色在 `backend/core/roles.py` 和 `frontend/src/store.js` 中声明。计算状态在 worker、queueing、API 和同一前端 store 中使用。

## 页面与接口

| 业务任务 | FastAPI 路由 | 页面 |
|---|---|---|
| 冰雕柜格档位 | `/cold_cells` /cold_cells/set-cell-state | `frontend/src/pages/cold_cells.js` |
| 空载与冰雕实测 | `/thaw_samples` /thaw_samples/observe-seam | `frontend/src/pages/thaw_samples.js` |
| 融缝稠密程度 | `/seam_maps` /seam_maps/score-seam，/seam_maps/record-seam | `frontend/src/pages/seam_maps.js` |
| 冰雕跨格互换单 | `/cell_swaps` /cell_swaps/reserve-swap，/cell_swaps/confirm-swap | `frontend/src/pages/cell_swaps.js` |

SQL 实体与约束在 `backend/domain` 下维护。前端使用原生 ES modules。核心算子为 KNN 密度反比。标准化后以四近邻平均距离的反比给出局部相对密度，按八条独立历史的 15% 分位设置比较阈值。

记录均为冰雕组的模拟交接数据，密度分用于排队复核。

[MIT](LICENSE)
