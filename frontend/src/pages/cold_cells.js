        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "旧模与冰雕成品柜格",
  "module": "冰雕柜格档位",
  "caption": "冰雕柜格档位",
  "detail": "柜格位置按用途独立挂牌，开放状态控制接收和换格。",
  "path": "/cold_cells",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "duty",
      "label": "功能区"
    },
    {
      "name": "authorized",
      "label": "点位已授权"
    },
    {
      "name": "free_slots",
      "label": "余位"
    },
    {
      "name": "closed",
      "label": "停止使用"
    }
  ],
  "layout": "flip",
  "view": "grid",
  "actions": [
    {
      "name": "set_cell_state",
      "label": "登记柜格暂停",
      "path": "/cold_cells/set-cell-state",
      "fields": [
        {
          "name": "cell",
          "label": "格位号",
          "kind": "text",
          "initial": "CELL-M"
        },
        {
          "name": "closed",
          "label": "停止使用",
          "kind": "bool",
          "initial": true
        }
      ],
      "help": "保留挂签用途，调整暂停状态。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "cold_cells";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
