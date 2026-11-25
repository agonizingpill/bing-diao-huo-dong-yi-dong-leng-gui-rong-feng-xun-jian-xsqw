        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "成品转运格互换",
  "module": "冰雕跨格互换单",
  "caption": "冰雕跨格互换单",
  "detail": "互换需核对成品槽位、类别和双签；锁定接收余位后，现场回执将余位返还到原柜格。",
  "path": "/cell_swaps",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "seam",
      "label": "融缝复核"
    },
    {
      "name": "target",
      "label": "目标柜格"
    },
    {
      "name": "handover",
      "label": "现场双签"
    },
    {
      "name": "state",
      "label": "状态"
    }
  ],
  "layout": "flip",
  "view": "stack",
  "actions": [
    {
      "name": "reserve_swap",
      "label": "锁定替换柜格",
      "path": "/cell_swaps/reserve-swap",
      "fields": [
        {
          "name": "code",
          "label": "互换单号",
          "kind": "text",
          "initial": "SWP-24"
        },
        {
          "name": "seam",
          "label": "融缝单号",
          "kind": "text",
          "initial": "DENS-24"
        },
        {
          "name": "target",
          "label": "目标柜格",
          "kind": "text",
          "initial": "CELL-B"
        },
        {
          "name": "handover",
          "label": "两位搬移人",
          "kind": "text",
          "initial": "江峰/罗岚"
        }
      ],
      "help": "目标柜格余位需先锁定。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "confirm_swap",
      "label": "收回换格凭条",
      "path": "/cell_swaps/confirm-swap",
      "fields": [
        {
          "name": "swap",
          "label": "互换单号",
          "kind": "text",
          "initial": "SWP-24"
        },
        {
          "name": "stamp",
          "label": "格签回执",
          "kind": "text",
          "initial": "CELL-B/2416"
        }
      ],
      "help": "交换到位后归还原柜格余位。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "cell_swaps";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
