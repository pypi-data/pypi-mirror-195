import numpy as np

from sklearn.metrics import accuracy_score, brier_score_loss
import robustness_metrics
from robustness_metrics.metrics import uncertainty
from sklearn.metrics import confusion_matrix



class SZ_Calibration_Metric:

    def get_performance_metrics(y_pred, y_true, loss=float('nan')):

        true_negatives,false_positives,false_negatives , true_positives = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

        accuracy = (true_positives + true_negatives) / len(y_true)
        assert not np.isnan(true_negatives)
        assert not np.isnan(false_positives)
        assert not np.isnan(false_negatives)
        assert not np.isnan(true_positives)

        if true_positives > 0:
            
            precision = true_positives / (true_positives + false_positives)
            recall = true_positives / (true_positives + false_negatives)
            f1_score = 2 * ((precision * recall) / (precision + recall))

            '''Intersection over Union (IoU) is used when calculating mAP. 
            It is a number from 0 to 1 that specifies the amount of overlap between the predicted and 
            ground truth bounding box. IoU is an important accuracy measure to track
            when gathering human annotations.
            '''
            iou = true_positives / (true_positives + false_positives + false_negatives)

        else:
            precision = recall = f1_score = iou = float('NaN')


        
        
        return {
            "Accuracy": accuracy,
            "TN": true_negatives,
            "FP": false_positives,
            "FN": false_negatives,
            "TP": true_positives,
            "Precision": precision,
            "Recall": recall,
            "F1_score": f1_score,
            "iou": iou,
            "True_mean": np.mean(y_true),
            "Pred_mean": np.mean(y_pred),
           
        }

    def get_ue_metrics(labels , logits, confidence = None):

        y_pred = np.argmax(logits, axis=1)

        if confidence is None:
            confidence = np.max(logits, axis=1)
        
        # labels = [1 if x=="yes" else 0 for x in dataframe["label"]]

        result_acc = accuracy_score(labels, y_pred)

        ece_calibrated = robustness_metrics.metrics.ExpectedCalibrationError(num_bins=2) 
        ece_calibrated.add_batch(model_predictions=logits, label=labels)
        result_ece = ece_calibrated.result()['ece']
        
        fixed_calibration_auroc = uncertainty._KerasCalibrationAUCMetric(curve='ROC', correct_pred_as_pos_label=False)
        fixed_calibration_auroc.update_state(y_true=labels, y_pred=y_pred, confidence=confidence)
        result_calibration_auroc = float(fixed_calibration_auroc.result())

        fixed_calibration_auprc = uncertainty._KerasCalibrationAUCMetric(curve='PR', correct_pred_as_pos_label=False)
        fixed_calibration_auprc.update_state(y_true=labels, y_pred=y_pred, confidence=confidence)
        result_calibration_auprc =  float(fixed_calibration_auprc.result())

        return {
            "ACC ":result_acc, 
            "ECE ":result_ece, 
            "AUROC ":result_calibration_auroc, 
            "AUPRC ":result_calibration_auprc
        }
    

    def get_ece(labels,logits):

        ece_calibrated = robustness_metrics.metrics.ExpectedCalibrationError(num_bins=2) 
        ece_calibrated.add_batch(model_predictions=logits, label=labels)
        result_ece = ece_calibrated.result()['ece']

        return {
            "ECE ":result_ece, 
        }
    

    def get_auroc(labels,logits, confidence = None):

        y_pred = np.argmax(logits, axis=1)

        if confidence is None:
            confidence = np.max(logits, axis=1)

        fixed_calibration_auroc = uncertainty._KerasCalibrationAUCMetric(curve='ROC', correct_pred_as_pos_label=False)
        fixed_calibration_auroc.update_state(y_true=labels, y_pred=y_pred, confidence=confidence)
        result_calibration_auroc = float(fixed_calibration_auroc.result())

        return {
            "AUROC ":result_calibration_auroc
        }
    
    def get_auprc(labels,logits, confidence = None):
        y_pred = np.argmax(logits, axis=1)

        if confidence is None:
            confidence = np.max(logits, axis=1)

        fixed_calibration_auprc = uncertainty._KerasCalibrationAUCMetric(curve='PR', correct_pred_as_pos_label=False)
        fixed_calibration_auprc.update_state(y_true=labels, y_pred=y_pred, confidence=confidence)
        result_calibration_auprc =  float(fixed_calibration_auprc.result())

        return {
            "AUPRC ":result_calibration_auprc
               }