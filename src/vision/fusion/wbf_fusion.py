from ensemble_boxes import weighted_boxes_fusion

def fuse_boxes(boxes_list, scores_list, labels_list, weights=None):
    fused_boxes, fused_scores, fused_labels = weighted_boxes_fusion(
        boxes_list, scores_list, labels_list, weights=weights,
        iou_thr=0.5, skip_box_thr=0.001
    )
    return fused_boxes, fused_scores, fused_labels
