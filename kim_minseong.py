# kim_minseong.py
# 이 파일은 김민성님의 유전병 계산기 관련 함수들을 포함합니다.

from collections import Counter, defaultdict
from itertools import product
import do_eunbi

# ------------------ [3] 유전병 계산기 함수들 (김민성) ------------------ #

# 코드 작성 및 수정: 김민성
def input_disease_info():
    is_sex_linked_str = do_eunbi.get_valid_input(
        "▶ 이 유전병은 성염색체 연관인가요? (y: 성염색체, n: 상염색체): ",
        lambda x: x.lower() in ['y', 'n'],
        "y 또는 n으로 입력해주세요."
    ).lower()
    is_sex_linked = (is_sex_linked_str == 'y')

    if is_sex_linked:
        while True:
            allele_location = input("▶ 보인자 알렐은 X 염색체에 있나요, Y 염색체에 있나요? (x 또는 y): ").strip().lower()
            if allele_location == 'x':
                disease_allele = "X'"
                break
            elif allele_location == 'y':
                disease_allele = "Y'"
                break
            else:
                print("  x 또는 y로 입력해주세요.")
    else:
        disease_allele = do_eunbi.get_valid_input( # 도은비님의 함수 호출
            "▶ 유전병 보인자 알렐을 2글자 형식으로 입력하세요 (예: A'): ",
            lambda x: len(x) == 2 and x[0].isalpha() and x[1] == "'",
            "예) A' 와 같은 2글자를 입력하세요 (첫 글자는 알파벳, 두 번째 글자는 어포스트로피)."
        ).upper()

    is_dominant_str = do_eunbi.get_valid_input( # 도은비님의 함수 호출
        "▶ 보인자 알렐은 우성인가요? 열성인가요? (우성:y, 열성:n): ",
        lambda x: x.lower() in ['y', 'n'],
        "y 또는 n으로 입력해주세요."
    ).lower()
    is_dominant = (is_dominant_str == 'y')

    return disease_allele, is_dominant, is_sex_linked


# 코드 작성 및 수정: 김민성
def input_parent_genotype_disease(is_sex_linked, disease_allele):
    mom_genotype = ""
    dad_genotype = ""

    if is_sex_linked:
        print("\n▶ 부모 유전자형 입력 (여성: XX, XX', X'X', 남성: XY, X'Y, XY') - x염색체에 있는 경우 X'이 보인자이며, y염색체에 있는 경우 Y'이 보인자입니다.")

        if disease_allele == "X'":
            while True:
                mom_input = input("  엄마 유전자형 입력 (예: XX, XX', X'X): ").strip().upper()
                if mom_input in ['XX', "XX'", "X'X'", "X'X"]:
                    mom_genotype = mom_input
                    break
                print("  엄마 유전자형은 XX, XX', X'X' 중 하나여야 합니다.")

            while True:
                dad_input = input("  아빠 유전자형 입력 (예: XY, X'Y): ").strip().upper()
                if dad_input in ['XY', "X'Y"]:
                    dad_genotype = dad_input
                    break
                print("  아빠 유전자형은 XY, X'Y 형식만 가능합니다 (X-연관 유전이므로 XY'는 입력할 수 없습니다).")

        elif disease_allele == "Y'":
            while True:
                mom_input = input("  엄마 유전자형 입력 (예: XX): ").strip().upper()
                if mom_input == 'XX':
                    mom_genotype = mom_input
                    break
                print("  엄마 유전자형은 XX여야 합니다 (Y-연관 유전이므로 XX'나 X'X'는 입력할 수 없습니다).")

            while True:
                dad_input = input("  아빠 유전자형 입력 (예: XY, XY'): ").strip().upper()
                if dad_input in ['XY', "XY'"]:
                    dad_genotype = dad_input
                    break
                print("  아빠 유전자형은 XY, XY' 형식만 가능합니다.")

    else:
        print("▶ 부모 유전자형 입력 (상염색체, 예: AA, Aa, A'A')")
        mom_genotype = do_eunbi.get_valid_input( # 도은비님의 함수 호출
            "  엄마 유전자형 입력: ",
            lambda x: len(x) >= 2 and all(c.isalpha() or c == "'" for c in x),
            "알파벳 또는 '로 이루어진 유전자형을 입력하세요 (최소 2글자)."
        ).upper()
        dad_genotype = do_eunbi.get_valid_input( # 도은비님의 함수 호출
            "  아빠 유전자형 입력: ",
            lambda x: len(x) >= 2 and all(c.isalpha() or c == "'" for c in x),
            "알파벳 또는 '로 이루어진 유전자형을 입력하세요 (최소 2글자)."
        ).upper()

    return mom_genotype, dad_genotype


# 코드 작성 및 수정: 김민성
def extract_alleles_autosomal(genotype, disease_allele):
    """상염색체 유전자형에서 대립유전자를 추출합니다."""
    alleles = []
    i = 0
    while i < len(genotype):
        if i + len(disease_allele) <= len(genotype) and genotype[i:i + len(disease_allele)] == disease_allele:
            alleles.append(disease_allele)
            i += len(disease_allele)
        elif i + 1 <= len(genotype) and genotype[i].isalpha():
            alleles.append(genotype[i])
            i += 1
        else:
            i += 1
    return alleles


# 코드 작성 및 수정: 김민성
def classify_sex_linked(genotype_str, disease_allele, is_dominant, sex):
    count = genotype_str.count(disease_allele)

    if is_dominant:
        return "환자" if count >= 1 else "정상"
    else:
        if sex == 'F':
            if disease_allele == "X'":
                if count == 2:
                    return "환자"
                elif count == 1:
                    return "보인자"
                else:
                    return "정상"
            else: # Y' 인데 여자면 무조건 정상 (여자는 Y가 없음)
                return "정상"
        else: # 남성 (XY 또는 X'Y 또는 XY')
            return "환자" if count >= 1 else "정상"


# 코드 작성 및 수정: 김민성
def classify_autosomal(genotype, disease_allele, is_dominant):
    num_disease_alleles = 0
    i = 0
    while i < len(genotype):
        if i + len(disease_allele) <= len(genotype) and genotype[i:i + len(disease_allele)] == disease_allele:
            num_disease_alleles += 1
            i += len(disease_allele)
        else:
            i += 1

    if is_dominant:
        return "환자" if num_disease_alleles >= 1 else "정상"
    else:
        if num_disease_alleles == 2:
            return "환자"
        elif num_disease_alleles == 1:
            return "보인자"
        else:
            return "정상"


# 코드 작성 및 수정: 김민성
def calculate_offspring_disease_autosomal(mom_genotype, dad_genotype, disease_allele):
    mom_alleles = extract_alleles_autosomal(mom_genotype, disease_allele)
    dad_alleles = extract_alleles_autosomal(dad_genotype, disease_allele)

    offspring_genotypes = Counter()
    for m_allele in mom_alleles:
        for d_allele in dad_alleles:
            offspring_geno = ''.join(sorted([m_allele, d_allele]))
            offspring_genotypes[offspring_geno] += 1

    total_offspring_combinations = len(mom_alleles) * len(dad_alleles)
    result_probs = {
        geno: (count / total_offspring_combinations) * 100
        for geno, count in offspring_genotypes.items()
    }
    return result_probs


# 코드 작성 및 수정: 김민성
def calculate_offspring_disease_sex_linked(mom_genotype, dad_genotype, disease_allele):
    offspring_results = defaultdict(float)

    # 엄마의 X 염색체 정보 파싱
    mom_x_chromosomes = []
    if mom_genotype == "XX":
        mom_x_chromosomes = ['X', 'X']
    elif mom_genotype == "XX'":
        mom_x_chromosomes = ['X', "X'"]
    elif mom_genotype == "X'X'":
        mom_x_chromosomes = ["X'", "X'"]
    elif mom_genotype == "X'X": # XX'와 동일하게 처리
        mom_x_chromosomes = ["X'", "X"]
    else:
        print(" 잘못된 엄마 유전자형입니다.")
        return {} # 잘못된 경우 빈 딕셔너리 반환

    # 아빠의 X, Y 염색체 정보 파싱
    dad_x_gamete = None
    dad_y_gamete = None

    if dad_genotype == "XY":
        dad_x_gamete = "X"
        dad_y_gamete = "Y"
    elif dad_genotype == "X'Y":
        dad_x_gamete = "X'"
        dad_y_gamete = "Y"
    elif dad_genotype == "XY'":
        dad_x_gamete = "X"
        dad_y_gamete = "Y'"
    else:
        print(" 잘못된 아빠 유전자형입니다.")
        return {} # 잘못된 경우 빈 딕셔너리 반환

    # 자손 유전자형 조합
    for mom_x in mom_x_chromosomes:
        # 딸 (엄마의 X + 아빠의 X)
        if dad_x_gamete: # 아빠가 X 염색체를 제공할 수 있을 때만 (항상 가능)
            alleles = sorted([mom_x, dad_x_gamete])
            genotype = ''.join(alleles)
            offspring_results[('F', genotype)] += 1

        # 아들 (엄마의 X + 아빠의 Y)
        if dad_y_gamete: # 아빠가 Y 염색체를 제공할 수 있을 때만 (항상 가능)
            genotype = mom_x + dad_y_gamete
            offspring_results[('M', genotype)] += 1

    total = len(mom_x_chromosomes) * 2 # 엄마의 X 2개 * 아빠의 감수분열 2개 (X, Y)
    if total == 0:
        return {}

    final_results = {
        (sex, geno): (count / total) * 100
        for (sex, geno), count in offspring_results.items()
    }
    return final_results

# 코드 작성 및 수정: 김민성
def disease_main():
    print("\n--- 유전병 확률 계산기 ---")
    disease_allele, is_dominant, is_sex_linked = input_disease_info()
    mom_genotype, dad_genotype = input_parent_genotype_disease(is_sex_linked, disease_allele)

    print("\n--- 자손 유전자형 및 환자/보인자/정상 확률 ---")
    if is_sex_linked:
        offspring_probs = calculate_offspring_disease_sex_linked(mom_genotype, dad_genotype, disease_allele)
        status_counts = defaultdict(float)
        female_patient_prob = 0.0
        male_patient_prob = 0.0
        total_females_prob_sum = 0.0 # 여자 자녀 전체 확률 합
        total_males_prob_sum = 0.0  # 남자 자녀 전체 확률 합


        if not offspring_probs:
            print("계산 가능한 자손 조합이 없습니다. 부모 유전자형을 확인해주세요.")
            return

        for (sex, geno), prob in offspring_probs.items():
            status = classify_sex_linked(geno, disease_allele, is_dominant, sex)
            print(f"  {sex} 자식 {geno}: {prob:.2f}% → {status}")
            status_counts[status] += prob

            if sex == 'F':
                total_females_prob_sum += prob
                if status == "환자":
                    female_patient_prob += prob
            elif sex == 'M':
                total_males_prob_sum += prob
                if status == "환자":
                    male_patient_prob += prob

        print("\n--- 총 확률 ---")
        total_overall_prob_sum = sum(status_counts.values())
        if total_overall_prob_sum > 0:
            for k, v in status_counts.items():
                print(f"  {k}: {(v / total_overall_prob_sum) * 100:.2f}%")
        else:
            print("계산된 확률이 없습니다.")


        print("\n--- 성별에 따른 환자 확률 ---")
        if total_females_prob_sum > 0:
            print(f"  여자 자녀 중 환자일 확률: {(female_patient_prob / total_females_prob_sum) * 100:.2f}%")
        else:
            print("  여자 자녀가 태어날 확률이 없습니다.")

        if total_males_prob_sum > 0:
            print(f"  남자 자녀 중 환자일 확률: {(male_patient_prob / total_males_prob_sum) * 100:.2f}%")
        else:
            print("  남자 자녀가 태어날 확률이 없습니다.")

    else: # 상염색체 유전병
        offspring_probs = calculate_offspring_disease_autosomal(mom_genotype, dad_genotype, disease_allele)
        status_counts = defaultdict(float)

        if not offspring_probs:
            print("계산 가능한 자손 조합이 없습니다. 부모 유전자형을 확인해주세요.")
            return

        for geno, prob in offspring_probs.items():
            status = classify_autosomal(geno, disease_allele, is_dominant)
            print(f"  {geno}: {prob:.2f}% → {status}")
            status_counts[status] += prob

        print("\n--- 총 확률 ---")
        total_overall_prob_sum = sum(status_counts.values())
        if total_overall_prob_sum > 0:
            for k, v in status_counts.items():
                print(f"  {k}: {(v / total_overall_prob_sum) * 100:.2f}%")
        else:
            print("계산된 확률이 없습니다.")
    print()
