        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "带载融缝的邻域密度",
  "module": "融缝稠密程度",
  "caption": "融缝稠密程度",
  "detail": "将同格带载历史换成标准化特征，近邻越远说明当前形态越少见。",
  "path": "/seam_maps",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "sample",
      "label": "冰雕实测"
    },
    {
      "name": "density",
      "label": "局部相对密度"
    },
    {
      "name": "threshold",
      "label": "基线门槛"
    },
    {
      "name": "decision",
      "label": "人工复核指向"
    },
    {
      "name": "token",
      "label": "计算凭据"
    }
  ],
  "layout": "split",
  "view": "grid",
  "actions": [
    {
      "name": "score_seam",
      "label": "计算带载局部密度",
      "path": "/seam_maps/score-seam",
      "fields": [
        {
          "name": "sample",
          "label": "观测号",
          "kind": "text",
          "initial": "ICE-X"
        }
      ],
      "help": "密度基于近邻距离的反比。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "record_seam",
      "label": "复核融缝提示",
      "path": "/seam_maps/record-seam",
      "fields": [
        {
          "name": "code",
          "label": "融缝单号",
          "kind": "text",
          "initial": "DENS-24"
        },
        {
          "name": "token",
          "label": "计算凭据",
          "kind": "token",
          "initial": ""
        }
      ],
      "help": "将算法输出与本次冰雕关联。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "seam_maps";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
