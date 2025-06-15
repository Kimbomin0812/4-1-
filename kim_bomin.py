# kim_bomin.py
# 이 파일은 김보민님의 완전우성/불완전우성/공우성 형질 정보 입력, 표현형 계산기 주 로직,
# 설명 페이지, 그리고 프로그램의 메인 메뉴 출력 및 선택을 받는 함수를 포함합니다.

from collections import Counter, defaultdict
from itertools import product
import do_eunbi 

# ------------------ [2] 표현형 계산기 입력 함수들 (김보민) ------------------ #

# 코드 작성 및 수정: 김보민
def 완전우성():  # 완전우성에 대한 정보를 입력받음
    alleles = []
    allele_traits = {}
    dominant_alleles = []
    recessive_alleles = []

    print("   완전 우성을 선택했으므로 대립유전자 수는 자동으로 2개로 설정됩니다.")

    dominant_a = do_eunbi.get_valid_input(
        "  우성 대립유전자 이름 입력 (한 글자, 중복 불가, 예: A): ",
        lambda x: len(x) == 1 and x.isalpha() and x not in alleles,
        "한 글자의 알파벳만 입력할 수 있으며, 이미 입력된 대립유전자와 중복될 수 없습니다."
    )
    alleles.append(dominant_a)
    dominant_alleles.append(dominant_a)
    tname_dominant = do_eunbi.get_valid_input(
        f"    '{dominant_a}'가 나타내는 형질 이름 입력 (예: 파란눈, 비워두면 기본 이름 사용): ",
        lambda x: True,
        ""
    )
    if not tname_dominant:
        tname_dominant = f"형질_{dominant_a}"
    allele_traits[dominant_a] = tname_dominant

    recessive_a = do_eunbi.get_valid_input(
        "  열성 대립유전자 이름 입력 (한 글자, 중복 불가, 예: a): ",
        lambda x: len(x) == 1 and x.isalpha() and x not in alleles,
        "한 글자의 알파벳만 입력할 수 있으며, 이미 입력된 대립유전자와 중복될 수 없습니다."
    )
    alleles.append(recessive_a)
    recessive_alleles.append(recessive_a)
    tname_recessive = do_eunbi.get_valid_input(
        f"    '{recessive_a}'가 나타내는 형질 이름 입력 (예: 초록눈, 비워두면 기본 이름 사용): ",
        lambda x: True,
        ""
    )
    if not tname_recessive:
        tname_recessive = f"형질_{recessive_a}"
    allele_traits[recessive_a] = tname_recessive

    return {
        'alleles': alleles,
        'allele_traits': allele_traits,
        'dominance_type': 1,  # 완전 우성
        'dominant_alleles': dominant_alleles,
        'recessive_alleles': recessive_alleles,
        'incomplete_dominance_traits': {},
        'heterozygous_phenotypes': {}
    }

# 코드 작성 및 수정: 김보민
def 불완전우성():  # 불완전우성 형질에 대한 정보 입력
    alleles = []
    allele_traits = {}
    incomplete_dominance_traits = {}

    print("   불완전 우성을 선택했으므로 대립유전자 수는 자동으로 2개로 설정됩니다.")

    a1 = do_eunbi.get_valid_input(
        "  첫 번째 대립유전자 이름 입력 (한 글자, 중복 불가, 예: R): ",
        lambda x: len(x) == 1 and x.isalpha() and x not in alleles,
        "한 글자의 알파벳만 입력할 수 있으며, 이미 입력된 대립유전자와 중복될 수 없습니다."
    )
    alleles.append(a1)
    tname1 = do_eunbi.get_valid_input(
        f"    '{a1}'가 나타내는 형질 이름 입력 (예: 붉은색): ",
        lambda x: bool(x.strip()),
        "형질 이름을 입력해주세요."
    )
    allele_traits[a1] = tname1

    a2 = do_eunbi.get_valid_input(
        "  두 번째 대립유전자 이름 입력 (한 글자, 중복 불가, 예: W): ",
        lambda x: len(x) == 1 and x.isalpha() and x not in alleles,
        "한 글자의 알파벳만 입력할 수 있으며, 이미 입력된 대립유전자와 중복될 수 없습니다."
    )
    alleles.append(a2)
    tname2 = do_eunbi.get_valid_input(
        f"    '{a2}'가 나타내는 형질 이름 입력 (예: 흰색): ",
        lambda x: bool(x.strip()),
        "형질 이름을 입력해주세요."
    )
    allele_traits[a2] = tname2

    combined_trait = do_eunbi.get_valid_input(
        f"  '{a1}{a2}' 이형접합일 때 나타나는 형질을 입력하세요 (예: 분홍색): ",
        lambda x: bool(x.strip()),
        "형질 이름을 입력해주세요."
    )
    incomplete_dominance_traits[frozenset(sorted([a1, a2]))] = combined_trait

    return {
        'alleles': alleles,
        'allele_traits': allele_traits,
        'dominance_type': 2,  # 불완전 우성
        'dominant_alleles': [],
        'recessive_alleles': [],
        'incomplete_dominance_traits': incomplete_dominance_traits,
        'heterozygous_phenotypes': {}
    }

# 코드 작성 및 수정: 김보민
def 공우성():  # 공우성 형질에 대한 입력
    alleles = []
    allele_traits = {}
    heterozygous_phenotypes = {}

    while True:
        try:
            m = int(do_eunbi.get_valid_input(
                "  대립유전자 수 입력 (예: 2 이상, ABO는 3): ",
                lambda x: x.isdigit() and int(x) >= 2,
                "2 이상의 숫자를 입력해주세요."
            ))
            break
        except ValueError:
            print("숫자를 입력해주세요.")

    print("\n  --- 각 대립유전자가 동형접합일 때의 표현형 입력 ---")
    for j in range(1, m + 1):
        a = do_eunbi.get_valid_input(
            f"  대립유전자 {j} 이름 입력 (한 글자, 중복 불가, 예: A, B, O): ",
            lambda x: len(x) == 1 and x.isalpha() and x.upper() not in [al.upper() for al in alleles],
            "한 글자의 알파벳만 입력할 수 있으며, 이미 입력된 대립유전자와 중복될 수 없습니다."
        )
        alleles.append(a)

        tname = do_eunbi.get_valid_input(
            f"    '{a}{a}' 또는 '{a}'가 단독으로 나타내는 형질 이름 입력 (예: A형, B형, O형): ",
            lambda x: bool(x.strip()),
            "형질 이름을 입력해주세요."
        )
        allele_traits[a] = tname

    print("\n  --- 이형접합 유전자형의 표현형 입력 ---")
    print("  (예: 'AB' 유전자형에 'AB형' 입력, 'AO' 유전자형에 'A형' 입력)")
    all_combinations = list(product(alleles, repeat=2))
    processed_combinations = set()

    for a1, a2 in all_combinations:
        if a1 == a2:
            continue

        sorted_combination = tuple(sorted([a1, a2]))
        if sorted_combination in processed_combinations:
            continue
        processed_combinations.add(sorted_combination)

        combo_str = ''.join(sorted([a1, a2]))
        pheno_input = do_eunbi.get_valid_input(
            f"  유전자형 '{combo_str}'이(가) 나타내는 표현형을 입력하세요 (예: AB형, A형): ",
            lambda x: bool(x.strip()),
            "표현형 이름을 입력해주세요."
        )
        heterozygous_phenotypes[frozenset(sorted_combination)] = pheno_input

    return {
        'alleles': alleles,
        'allele_traits': allele_traits,
        'dominance_type': 3,  # 공우성
        'dominant_alleles': [],
        'recessive_alleles': [],
        'incomplete_dominance_traits': {},
        'heterozygous_phenotypes': heterozygous_phenotypes
    }


# 코드 작성 및 수정: 김보민
def cross_phenotype_prob(mom_alleles, dad_alleles, trait):
    mom_gametes = [mom_alleles[0], mom_alleles[1]]
    dad_gametes = [dad_alleles[0], dad_alleles[1]]

    offspring_genotypes = []
    for m_gamete in mom_gametes:
        for d_gamete in dad_gametes:
            offspring_genotypes.append(''.join(sorted([m_gamete, d_gamete])))

    total_offspring = len(offspring_genotypes)
    phenotype_counts = Counter()
    genotype_counts = Counter()

    if trait['dominance_type'] == 1:
        get_phenotype_func = do_eunbi.get_phenotype_complete_dominance 
    elif trait['dominance_type'] == 2:
        get_phenotype_func = do_eunbi.get_phenotype_incomplete_dominance 
    else:
        get_phenotype_func = do_eunbi.get_phenotype_codominance 

    for geno in offspring_genotypes:
        pheno = get_phenotype_func(geno, trait)
        phenotype_counts[pheno] += 1
        genotype_counts[geno] += 1

    phenotype_probs = {pheno: (count / total_offspring) * 100 for pheno, count in phenotype_counts.items()}
    genotype_probs = {geno: (count / total_offspring) * 100 for geno, count in genotype_counts.items()}

    return genotype_probs, phenotype_probs

# 코드 작성 및 수정: 김보민 (표현형 계산기 주 로직)
def phenotype_main():
    print("\n--- 표현형 확률 계산기 ---")
    traits = do_eunbi.input_phenotype_info(완전우성, 불완전우성, 공우성)
    mom_genes, dad_genes = do_eunbi.input_parents_phenotypes(traits) 

    print("\n--- 자손 유전자형 및 표현형 확률 (각 형질별) ---")
    for i, trait in enumerate(traits, start=1):
        mom_trait_gene = mom_genes[i - 1]
        dad_trait_gene = dad_genes[i - 1]

        mom_alleles = list(mom_trait_gene)
        dad_alleles = list(dad_trait_gene)

        genotype_probs, phenotype_probs = cross_phenotype_prob(mom_alleles, dad_alleles, trait)

        print(f"\n[{i}번째 형질]")
        print("  유전자형별 확률:")
        for geno, p in sorted(genotype_probs.items()):
            print(f"    {geno:<10}: {p:.2f}%")

        print("  표현형별 확률:")
        for pheno, p in sorted(phenotype_probs.items()):
            print(f"    {pheno:<20}: {p:.2f}%")
    print()

    # --- 추가: 전체 형질 조합 확률 계산 (유전자형) ---
    print("\n--- 전체 형질 조합 유전자형 확률 ---")

    all_genotype_prob_lists = []
    for i, trait in enumerate(traits, start=1):
        mom_trait_gene = mom_genes[i - 1]
        dad_trait_gene = dad_genes[i - 1]
        mom_alleles = list(mom_trait_gene)
        dad_alleles = list(dad_trait_gene)
        genotype_probs, _ = cross_phenotype_prob(mom_alleles, dad_alleles, trait)
        all_genotype_prob_lists.append(genotype_probs)

    genotype_options_per_trait = []
    for prob_dict in all_genotype_prob_lists:
        genotype_options_per_trait.append([(g, p / 100) for g, p in prob_dict.items()])

    combined_genotype_probs = defaultdict(float)

    for combination_tuple in product(*genotype_options_per_trait):
        combined_genotype_str = ""
        combined_probability = 1.0

        for genotype, prob in combination_tuple:
            combined_genotype_str += genotype
            combined_probability *= prob

        combined_genotype_probs[combined_genotype_str] += combined_probability * 100

    if combined_genotype_probs:
        for geno_combo, prob in sorted(combined_genotype_probs.items()):
            print(f"  {geno_combo:<15}: {prob:.2f}%")
    else:
        print("  계산 가능한 전체 형질 유전자형 조합이 없습니다.")

    # --- 추가: 전체 형질 조합 확률 계산 (표현형) ---
    print("\n--- 전체 형질 조합 표현형 확률 ---")

    all_phenotype_prob_lists = []
    for i, trait in enumerate(traits, start=1):
        mom_trait_gene = mom_genes[i - 1]
        dad_trait_gene = dad_genes[i - 1]
        mom_alleles = list(mom_trait_gene)
        dad_alleles = list(dad_trait_gene)
        _, phenotype_probs = cross_phenotype_prob(mom_alleles, dad_alleles, trait)
        all_phenotype_prob_lists.append(phenotype_probs)

    phenotype_options_per_trait = []
    for prob_dict in all_phenotype_prob_lists:
        phenotype_options_per_trait.append([(p_name, p / 100) for p_name, p in prob_dict.items()])

    combined_phenotype_probs = defaultdict(float)

    for combination_tuple in product(*phenotype_options_per_trait):
        combined_phenotype_str = ""
        combined_probability = 1.0

        phenotype_parts = []
        for phenotype_name, prob in combination_tuple:
            phenotype_parts.append(phenotype_name)
            combined_probability *= prob

        combined_phenotype_str = ", ".join(phenotype_parts)

        combined_phenotype_probs[combined_phenotype_str] += combined_probability * 100

    if combined_phenotype_probs:
        max_len = max(len(s) for s in combined_phenotype_probs.keys())
        for pheno_combo, prob in sorted(combined_phenotype_probs.items()):
            print(f"  {pheno_combo:<{max_len + 2}}: {prob:.2f}%")
    else:
        print("  계산 가능한 전체 형질 표현형 조합이 없습니다.")
    print()

# ------------------ [4] 설명 페이지 (김보민) ------------------ #
# 코드 작성 및 수정: 김보민
def show_explanation_page():
    print("\n--- 유전 및 유전병 설명 ---")
    print("\n## 1. 유전의 기본 원리")
    print("유전은 부모의 형질이 자손에게 전달되는 현상을 말한다. 여기서 '형질'은 눈 색깔, 혈액형 등 생물이 가진 특징을 의미한다. 이러한 형질을 결정하는 것이 바로 '유전자'이다.")
    print("\n### 대립유전자와 표현형")
    print("""  - 대립유전자 : 한 형질을 결정하는 여러 유전자 형태를 말한다.
               예를 들어 혈액형 A, B, O가 대립유전자이다.""")
    print("""  - 표현형 : 유전자형이 겉으로 드러나는 모습이나 특성을 말한다.
               예를 들어 혈액형 A형, B형 등이 표현형이다.""")
    print("\n### 우열 관계의 종류")
    print("  - 완전 우성 (Complete Dominance) :")
    print("""    두 대립유전자 중 하나(우성)가 다른 하나(열성)의 발현을 완전히 억제하여 우성 형질만 나타나는 경우이다.
    예를 들어 둥근 완두콩(R)과 주름진 완두콩(r)이 만나면, Rr 유전자형일 때 둥근 완두콩 표현형이 나타난다.""")
    print("  - 불완전 우성 (Incomplete Dominance):")
    print("""    두 대립유전자의 중간 형질이 나타나는 경우이다.
    예를 들어 붉은 꽃(RR)과 흰 꽃(WW)이 만나면, RW 유전자형일 때 분홍색 꽃이 나타난다.
    항상 두 대립유전자에서만 나타나는 것은 아니지만 대부분 두 대립유전자에서만 나타나기 때문에 이 프로그램에서는 두 대립유전자사이의 경우만 생각한다.""")
    print("  - 공우성 (Co-dominance / 복대립 유전):")
    print("""    두 대립유전자들이 모두 동등하게 발현되어 두 가지 형질이 동시에 나타나는 경우이다. "
    예를 들어 ABO 혈액형에서 A 대립유전자와 B 대립유전자가 만나면, AB형이라는 새로운 표현형이 나타나는데, 이는 A와 B 형질이 모두 발현된 것이다.""")

    print("\n## 2. 유전병의 종류")
    print("유전병은 특정 유전자의 이상으로 인해 발생하는 질병을 말한다.")
    print("\n### 상염색체 유전병")
    print("  - 성염색체를 제외한 나머지 염색체(상염색체)에 존재하는 유전자 이상으로 인해 발생한다. 남녀 모두에게 동일한 확률로 나타난다.")
    print("  - 우성 유전 : 하나의 이상 유전자만 있어도 질병이 발현된다. 예시: 헌팅턴병")
    print("  - 열성 유전 : 두 개의 이상 유전자가 모두 있을 때만 질병이 발현된다. 예시: 낭포성 섬유증, 겸상 적혈구 빈혈증")

    print("\n### 성염색체 유전병 (X-연관 유전, Y-연관 유전)")
    print("  - 성별을 결정하는 X 또는 Y 염색체에 존재하는 유전자 이상으로 인해 발생한다.")
    print("  - X-연관 유전 : X 염색체에 이상 유전자가 있을 때 발생한다. 남성은 X 염색체가 하나뿐이므로 여성보다 더 큰 영향을 받기 쉽다.")
    print("    - X-연관 우성 : 예시: 비타민 D 저항성 구루병")
    print("    - X-연관 열성 : 예시: 적록색맹, 혈우병")
    print("  - Y-연관 유전 : Y 염색체에 이상 유전자가 있을 때 발생한다. Y 염색체는 남성에게만 있으므로 남성에게만 나타난다.")
    print("    - 예시: 일부 불임 유전")

# ------------------ 메인 메뉴 출력 및 선택 함수 (김보민) ------------------ #
def display_main_menu_and_get_choice():
    print("\n--- 유전 계산기 메인 메뉴 ---")
    print("1. 표현형 확률 계산기")
    print("2. 유전병 확률 계산기")
    print("3. 유전 및 유전병 설명")
    print("4. 종료")
    choice = do_eunbi.get_valid_input( 
        "선택: ",
        lambda x: x in ['1', '2', '3', '4'],
        "1, 2, 3, 4 중 하나를 입력해주세요."
    )
    return choice
