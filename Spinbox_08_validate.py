import tkinter

window = tkinter.Tk()
window.title("Spinbox")
window.geometry("300x200")

# 입력안내 및 오류 안내용 lable 생성
# 초기 생성 내용은 "숫자를 입력하세요"
label = tkinter.Label(window, text="숫자를 입력하세요", height=3)
label.pack()


def value_check(self):
    # 입력 값의 유효성을 검사하기 위한 메소드 (True 또는 False 반환)
    label.config(text="숫자를 입력하세요.")
    valid = False
    if self.isdigit():                              # 숫자인지 판별(음수/소숫점 단위는 False)
        if (int(self) <= 50 and int(self) >= 0):    # 숫자 범위판별
            valid = True                            # 유효한 값일 때 True 반환
    elif self == "":                                # 공백일 때 유효함
        valid = True
    return valid                                    # 유효한 값이 아닐 때 False 반환


def value_error(self):
    # 입력 값이 유효하지 않을 때 실행할 메소드
    label.config(text=str(self) + "를 입력하셨습니다. \n올바른 값을 입력하세요.")


validate_command = (window.register(value_check), '%P')
# window.register()메소드를 통해 이미 생성된 객체인 window에 value_check함수를 적용
# %P 콜백을 value_check()의 parameter로 전달
# regisiter: 검사해줘. ()괄호 안의 내용으로 검사해줘!
# %P: 옵션, 약속임. 문제가 없으면 들어온 값으로 처리
invalid_command = (window.register(value_error), '%P')
# window.register()메소드를 통해 이미 생성된 객체인 window에 value_error함수를 적용
# %P 콜백을 value_check()의 parameter로 전달

spinbox = tkinter.Spinbox(window, from_=0, to=50, validate='all',
                          validatecommand=validate_command, invalidcommand=invalid_command)
# validatecommand=(튜플) 형식이며, return값이 False일 때, invalidcommand에 해당하는 메소드 실행

spinbox.pack()
window.mainloop()
