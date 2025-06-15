# do_eunbi.py
# 이 파일은 도은비님의 유틸리티 함수, 표현형 계산기 관련 입력 및 표현형 결정 함수를 포함합니다.

from collections import Counter, defaultdict
from itertools import product

# ------------------ [1] 유틸 함수 (도은비) ------------------ #
# 코드 작성 및 수정: 도은비
def get_valid_input(prompt, validation_func, error_message):  # 유효한 사용자입력만 받는 함수.
    while True:
        user_input = input(prompt).strip()
        if validation_func(user_input):
            return user_input
        print(f" {error_message}")

# 코드 작성 및 수정: 도은비
def get_valid_genotype(prompt, expected_length, allowed_chars=None):  # 특정 길이의 유전자형을 입력받고 검증
    def validate(x):
        if len(x) != expected_length:
            return False
        if allowed_chars:
            return all(c in allowed_chars for c in x)
        return all(c.isalpha() or c == "'" for c in x)

    error_message = f"정확히 {expected_length}글자의 "
    if allowed_chars:
        error_message += f"정의된 대립유전자 ({', '.join(allowed_chars)})만 사용하세요."
    else:
        error_message += "알파벳 또는 ' 만 입력하세요."

    return get_valid_input(
        prompt,
        validate,
        error_message
    )

# ------------------ [2] 표현형 계산기 관련 입력 및 결정 함수 (도은비) ------------------ #

# 코드 작성 및 수정: 도은비 
def input_phenotype_info(완전우성_func, 불완전우성_func, 공우성_func):
    while True:
        try:
            n = int(get_valid_input(
                "▶ 형질 개수를 입력하세요 (예: 2): ",
                lambda x: x.isdigit() and int(x) >= 1,
                "1 이상의 숫자를 입력해주세요."
            ))
            break
        except ValueError:
            print("숫자를 입력해주세요.")

    traits = []

    for i in range(1, n + 1):
        print(f"\n--- {i}번째 형질 정보 입력 ---")

        dominance_type = int(get_valid_input(
            "  표현형 유형 선택 (1: 완전우성, 2: 불완전 우성, 3: 공우성/복대립): ",
            lambda x: x in ['1', '2', '3'],
            "1, 2, 3 중 하나를 입력해주세요."
        ))

        if dominance_type == 1:
            traits.append(완전우성_func())
        elif dominance_type == 2:
            traits.append(불완전우성_func())
        else:  # dominance_type == 3 (공우성/복대립)
            traits.append(공우성_func())

    return traits

# 코드 작성 및 수정: 도은비 
def input_parents_phenotypes(traits):  # 각 형질별로 엄마, 아빠 유전자형 리스트로 반환
    mom_genes, dad_genes = [], []
    for idx, trait in enumerate(traits, start=1):
        allowed_alleles_for_validation = trait['alleles']

        mom_g = get_valid_input(
            f"▶ 엄마의 {idx}번째 형질 유전자형 입력 (2글자, 예: Aa 또는 AA): ",
            lambda x: len(x) == 2 and x[0] in allowed_alleles_for_validation and x[1] in allowed_alleles_for_validation,
            f"정확히 2글자의 알파벳으로 입력하고, 정의된 대립유전자 ({', '.join(allowed_alleles_for_validation)})만 사용하세요."
        )
        dad_g = get_valid_input(
            f"▶ 아빠의 {idx}번째 형질 유전자형 입력 (2글자, 예: Aa 또는 aa): ",
            lambda x: len(x) == 2 and x[0] in allowed_alleles_for_validation and x[1] in allowed_alleles_for_validation,
            f"정확히 2글자의 알파벳으로 입력하고, 정의된 대립유전자 ({', '.join(allowed_alleles_for_validation)})만 사용하세요."
        )
        mom_genes.append(mom_g)
        dad_genes.append(dad_g)
    return mom_genes, dad_genes

# 코드 작성 및 수정: 도은비
def get_phenotype_complete_dominance(geno_pair, trait):  # 완전 우성에서 표현형 반환
    a1, a2 = sorted(list(geno_pair))
    allele_traits = trait['allele_traits']
    dominant_alleles = trait['dominant_alleles']
    recessive_alleles = trait['recessive_alleles']

    for dominant_a in dominant_alleles:
        if dominant_a == a1 or dominant_a == a2:
            return allele_traits.get(dominant_a)

    if a1 == a2 and a1 in recessive_alleles:
        return allele_traits.get(a1)

    return "Unknown Phenotype (Complete Dominance)"

# 코드 작성 및 수정: 도은비
def get_phenotype_incomplete_dominance(geno_pair, trait):  # 불완전 우성에서 표현형 반환
    a1, a2 = sorted(list(geno_pair))
    allele_traits = trait['allele_traits']
    incomplete_dominance_traits = trait['incomplete_dominance_traits']

    if a1 == a2:  # 동형접합
        return allele_traits.get(a1)
    else:  # 이형접합
        combined_key = frozenset([a1, a2])
        return incomplete_dominance_traits.get(combined_key)

# 코드 작성 및 수정: 도은비
def get_phenotype_codominance(geno_pair, trait):  # 공우성에서 표현형 반환.
    a1, a2 = sorted(list(geno_pair))  # 유전자형을 정렬하여 키로 사용
    allele_traits = trait['allele_traits']
    heterozygous_phenotypes = trait['heterozygous_phenotypes']

    if a1 == a2:  # 동형접합 (예: AA, BB, OO)
        return allele_traits.get(a1)
    else:  # 이형접합 (예: AB, AO, BO)
        combined_key = frozenset(sorted([a1, a2])) # frozenset으로 변경하여 순서에 무관하게 키 생성
        if combined_key in heterozygous_phenotypes:
            return heterozygous_phenotypes.get(combined_key)
        else:
            return "Undefined Co-dominance Heterozygous"
