# main.py
# 이 파일은 전체 유전 계산기 프로그램의 통합 실행을 담당합니다.
# 김보민님의 display_main_menu_and_get_choice 함수를 사용하여 메뉴를 표시합니다.

import do_eunbi
import kim_bomin
import kim_minseong

def main():
    while True:
        choice = kim_bomin.display_main_menu_and_get_choice() # 김보민님의 메뉴 함수 호출

        if choice == '1':
            kim_bomin.phenotype_main() # 김보민님의 표현형 계산기 호출
        elif choice == '2':
            kim_minseong.disease_main() # 김민성님의 유전병 계산기 호출
        elif choice == '3':
            kim_bomin.show_explanation_page() # 김보민님의 설명 페이지 호출
        elif choice == '4':
            print("프로그램을 종료합니다.")
            break

if __name__ == "__main__":
    main()
