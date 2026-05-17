import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import precision_recall_curve, ConfusionMatrixDisplay

def plot_pr_curve_multiclass(y_true, y_scores, classes, target_class=None):
    """
    Будує Precision-Recall криву. 
    Якщо target_class вказано, будує криву (One-vs-Rest) лише для цього класу.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    classes_list = list(classes)
    
    if target_class:
        indices = [classes_list.index(target_class)]
    else:
        indices = range(len(classes_list))

    for i in indices:
        # Бінаризуємо мітки (1 для цільового класу, 0 для всіх інших)
        y_true_bin = (np.array(y_true) == classes_list[i]).astype(int)
        
        precision, recall, thresholds = precision_recall_curve(y_true_bin, y_scores[:, i])
        ax.plot(recall, precision, label=f'Class: {classes_list[i]}')

    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    title = f'Precision-Recall Curve ({target_class} vs Rest)' if target_class else 'Precision-Recall Curve'
    ax.set_title(title)
    ax.legend(loc="lower left")
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.show()

def apply_custom_threshold_multiclass(y_scores, classes, target_class, threshold=0.0):
    """
    Застосовує кастомний поріг для конкретного класу.
    Якщо впевненість для target_class > threshold, прогнозуємо його.
    Інакше прогнозуємо клас з найвищою оцінкою серед інших.
    """
    classes_list = list(classes)
    target_idx = classes_list.index(target_class)
    y_pred_custom = []
    
    for scores in y_scores:
        if scores[target_idx] > threshold:
            y_pred_custom.append(classes_list[target_idx])
        else:
            # Шукаємо максимум серед інших класів
            masked_scores = scores.copy()
            masked_scores[target_idx] = -np.inf
            best_other_idx = np.argmax(masked_scores)
            y_pred_custom.append(classes_list[best_other_idx])
            
    return np.array(y_pred_custom)

def plot_confusion_matrix(y_true, y_pred, classes, title='Confusion Matrix'):
    """
    Проста обгортка для малювання матриці помилок.
    """
    fig, ax = plt.subplots(figsize=(7, 6))
    ConfusionMatrixDisplay.from_predictions(
        y_true, 
        y_pred, 
        display_labels=classes, 
        cmap=plt.cm.Blues, 
        ax=ax, 
        values_format='d'
    )
    plt.title(title)
    plt.show()