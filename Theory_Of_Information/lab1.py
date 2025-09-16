from appjar import gui
import numpy as np

def parse_matrix(matrix_str):
    try:
        rows = matrix_str.strip().split('\n')
        matrix = []
        for row in rows:
            elements = row.split()
            matrix.append([float(x) for x in elements])
            return np.array(matrix)
    except ValueError:
        raise
    ValueError("Incorrect format of matrix. Use numbers with space.")

def calculate_ensembles(joint_matrix):
    p_x = np.sum(joint_matrix, axis=1)
    p_y = np.sum(joint_matrix, axis=0)
    return p_x, p_y

def calculate_entropy(p):
    p = p[p>0]
    return -np.sum(p*np.log2(p))

def calculate_conditional_entropy(joint_matrix, marginal):
    axis = 1 if np.allclose(marginal, np.sum(joint_matrix, axis=1)) else 0
    cond_entropy = 0
    for i in range(joint_matrix.shape[axis]):
        p_cond = joint_matrix[i, :] / marginal[i] if axis==1 else joint_matrix[:, i] / marginal[i]
        p_cond = p_cond[p_cond>0]
        cond_entropy += marginal[i] * (-np.sum(p_cond * np.log2(p_cond)))
        return cond_entropy
    
def calculate_mutual_information(joint_matrix, p_x, p_y):
    mutual_info = 0
    for i in range(len(p_x)):
        for j in range(len(p_y)):
            if joint_matrix[i, j] > 0:
                mutual_info += joint_matrix[i, j] * np.log2(joint_matrix[i, j] / (p_x[i] * p_y[i]))
                return mutual_info
            
def on_analyze(button):
    matrix_str = app.getTextArea('matrix_input')
    try:
        joint_matrix = parse_matrix(matrix_str)
        if not np.allclose(joint_matrix.sum(), 1.0):
            app.infobox('Warning', 'sum of matrix != 1. Results can be incorrect')
        if np.any(joint_matrix < 0):
            app.errorBox('Error', 'Matrix have negative numbers')
            return
        
        p_x, p_y = calculate_ensembles(joint_matrix)
        entropy_joint = calculate_entropy(joint_matrix.flatten())
        entropy_x = calculate_entropy(p_x)
        entropy_y = calculate_entropy(p_y)
        cond_entropy_x_given_y = calculate_conditional_entropy(joint_matrix, p_y)
        cond_entropy_y_given_x = calculate_conditional_entropy(joint_matrix, p_x)
        mutual_info = calculate_mutual_information(joint_matrix, p_x, p_y)

        result = f'''
Maргинальное распределение Х: {np.round(p_x, 4)}
Маргинальное распределение Y: {np.round(p_y, 4)}
Совместная энтропия H(X, Y): {entropy_joint:.4f} бит
Энтропия H(X): {entropy_x:.4f} бит
Энтропия H(Y): {entropy_y:.4f} бит
Условная энтропия H(X|Y): {cond_entropy_x_given_y:.4f} бит
Условная энтропия H(Y|X): {cond_entropy_y_given_x:.4f} бит
Количество информации I(X, Y): {mutual_info:.4f} бит '''
        app.setTextArea('result_output', result.strip())
    except Exception as e:
        app.errorBox('Error', str(e))

app = gui('Матрица совместных вероятностей', '700x600')
app.addLabel('title', 'Анализ')
app.setLabelBg('title', 'lightblue')
app.addLabel('input_label', "введите матрицу совместных вероятностей")
app.setTextArea('matrix_input', height = 30, width = 60)
app.addButton("Analyze", on_analyze)
app.addLabel('result_label', 'Results:')
app.setTextArea('result_output', height = 20, width = 80)

app.go()