from sklearn.metrics import roc_auc_score
import torch


def accuracy(pred, target):
    return (pred == target).sum().item() / len(target)


def true_positive(pred, target):
    return (target[pred == 1] == 1).sum().item()


def false_positive(pred, target):
    return (target[pred == 1] == 0).sum().item()


def true_negative(pred, target):
    return (target[pred == 0] == 0).sum().item()


def false_negative(pred, target):
    return (target[pred == 0] == 1).sum().item()


def recall(pred, target):
    """
    Or true positive rate.
    """
    try:
        return true_positive(pred, target) / (target == 1).sum().item()
    except:  # divide by zero
        return -1


def precision(pred, target):
    try:
        prec = true_positive(pred, target) / (pred == 1).sum().item()
        return prec
    except:  # divide by zero
        return -1


def f1_score(pred, target):
    prec = precision(pred, target)
    rec = recall(pred, target)
    try:
        return 2 * (prec * rec) / (prec + rec)
    except:
        return 0


def false_positive_rate(pred, target):
    try:
        return false_positive(pred, target) / (target == 0).sum().item()
    except:  # divide by zero
        return -1


def false_negative_rate(pred, target):
    """
    Or 1 - recall/true_positive_rate
    """
    try:
        return false_negative(pred, target) / (target == 1).sum().item()
    except:  # divide by zero
        return -1



def eval_metrics(target, pred_prob, threshold=0.5):

    if isinstance(target, torch.Tensor):
        target = target.cpu().numpy()
    if isinstance(pred_prob, torch.Tensor):
        pred_prob = pred_prob.cpu().numpy()

    pred = (pred_prob >= threshold).astype(int)

    acc = accuracy(pred, target)
    fpr = false_positive_rate(pred, target)
    fnr = false_negative_rate(pred, target)
    rec = recall(pred, target)
    prc = precision(pred, target)
    f1 = f1_score(pred, target)
    auroc = roc_auc_score(target, pred_prob)
    result_dict = {'acc': acc, 'fpr': fpr, 'fnr': fnr, 'rec': rec, 'prc': prc, 'f1': f1, 'auroc': auroc}

    return result_dict
