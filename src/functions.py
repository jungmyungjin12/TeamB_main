# 라이브러리 import
import os
with open('library.txt','r') as f:
    for library in f:
        exec(library)

def fit_data(X,Y,N):
    coef = np.polyfit(X, Y, N)
    func = np.poly1d(coef)
    fit_data = func(X)
    return fit_data

def R_square(X,Y,Y_reg): # R square 값을 계산하는 함수
    Y_mean=sum(Y)/Y.size # 전류의 평균값
    SST=sum((Y-Y_mean)**2) # 전체 데이터와 평균값 간 차이 제곱의 합
    SSE=sum((Y_reg-Y_mean)**2) # 추정값과 평균값 간 차이 제곱의 합
    SSR=sum((Y-Y_reg)**2)
    return 1-SSR/SST # R square 값을 반환

def Best_fit_R(X,Y): # 가장 R_sqaure가 1에 가까운 R_square 값을 반환하는 함수
    Rs = []
    for i in range(1,11):
        coef = np.polyfit(X,Y,i)
        func = np.poly1d(coef)
        fitted_data = func(X)
        Rs.append(R_square(X,Y,fitted_data))
    max_degree = Rs.index(max(Rs))+1
    return max(Rs)
def shockely_diode_IV_fit_R(V,I):
    def shockely_diode(voltage, rev_sat_I, n):
        k = 1.380649 * 10 ** (-23)
        q = 1.602 * 10 ** (-19)
        temp = 300
        return rev_sat_I * (np.exp(q * voltage / (n * k * temp)) - 1)

    # 모델 인스턴스 생성
    model = Model(shockely_diode)

    # 초기 매개 변수 설정
    params = model.make_params(
        rev_sat_I=1e-7,
        n=1
    )

    # 모델 피팅
    result = model.fit(I[10:], params, voltage=V[10:])
    # print(result.best_fit,'\n',result.best_values) # parameter 값과 근사된 데이터에 대한 값을 보여주는 코드
    coef = np.polyfit(V[:10],I[:10],9)
    func = np.poly1d(coef)
    fit_data = func(V[:10])
    fit_data = np.append(fit_data, result.best_fit)
    return float(str(R_square(V,I,fit_data))[:9])

def Ref_fitted_data(X,Y): # 가장 R_sqaure가 1에 가까운 R_square 값을 반환하는 함수
    Rs = []
    for i in range(1,11):
        coef = np.polyfit(X,Y,i)
        func = np.poly1d(coef)
        fitted_data = func(X)
        Rs.append(R_square(X,Y,fitted_data))
    max_degree = Rs.index(max(Rs))+1
    return fit_data(X,Y,max_degree)
