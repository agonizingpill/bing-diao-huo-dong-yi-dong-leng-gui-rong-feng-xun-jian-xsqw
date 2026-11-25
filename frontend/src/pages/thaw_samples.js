        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "空载基线和冰雕接缝观测",
  "module": "空载与冰雕实测",
  "caption": "空载与冰雕实测",
  "detail": "同一柜格独立保留空载窗与带载样。空载记录不参与成品融缝比较。",
  "path": "/thaw_samples",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "cell",
      "label": "柜格"
    },
    {
      "name": "mass_kg",
      "label": "冰灯质量 kg"
    },
    {
      "name": "melt",
      "label": "接缝偏移 mm"
    },
    {
      "name": "drift",
      "label": "相邻窗温漂"
    },
    {
      "name": "empty_test",
      "label": "空载测试"
    },
    {
      "name": "piece",
      "label": "冰雕码"
    }
  ],
  "layout": "stack",
  "view": "table",
  "actions": [
    {
      "name": "observe_seam",
      "label": "登记柜格观测",
      "path": "/thaw_samples/observe-seam",
      "fields": [
        {
          "name": "code",
          "label": "观测号",
          "kind": "text",
          "initial": "ICE-X"
        },
        {
          "name": "cell",
          "label": "格位号",
          "kind": "text",
          "initial": "CELL-A"
        },
        {
          "name": "mass_kg",
          "label": "冰灯质量 kg",
          "kind": "float",
          "initial": 24.2
        },
        {
          "name": "melt",
          "label": "接缝偏移 mm",
          "kind": "float",
          "initial": 4.2
        },
        {
          "name": "drift",
          "label": "相邻窗温漂",
          "kind": "float",
          "initial": 1.9
        },
        {
          "name": "empty_test",
          "label": "是否空载",
          "kind": "bool",
          "initial": false
        },
        {
          "name": "piece",
          "label": "冰雕块码",
          "kind": "text",
          "initial": "LAMP-11"
        }
      ],
      "help": "样本需记录状态和实物码。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "thaw_samples";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
