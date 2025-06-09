import timeit

def boyer_moore_search(text, pattern):
    def build_bad_char_table(pattern):
        table = {}
        for i in range(len(pattern)):
            table[pattern[i]] = len(pattern) - i - 1
        return table
    
    n = len(text)
    m = len(pattern)
    comparisons = 0
    
    if m == 0:
        return 0, 0
    
    bad_char = build_bad_char_table(pattern)
    i = 0
    
    while i <= n - m:
        j = m - 1
        
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
            comparisons += 1
        
        if j < 0:
            return i, comparisons
        
        comparisons += 1
        shift = bad_char.get(text[i + j], m)
        i += max(1, shift)
    
    return -1, comparisons

def kmp_search(text, pattern):
    def compute_prefix_function(pattern):
        m = len(pattern)
        pi = [0] * m
        j = 0
        
        for i in range(1, m):
            while j > 0 and pattern[i] != pattern[j]:
                j = pi[j - 1]
            
            if pattern[i] == pattern[j]:
                j += 1
            
            pi[i] = j
        
        return pi
    
    n = len(text)
    m = len(pattern)
    comparisons = 0
    
    if m == 0:
        return 0, 0
    
    pi = compute_prefix_function(pattern)
    j = 0
    
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
            comparisons += 1
        
        comparisons += 1
        if text[i] == pattern[j]:
            j += 1
        
        if j == m:
            return i - m + 1, comparisons
    
    return -1, comparisons

def rabin_karp_search(text, pattern):
    d = 256
    q = 101
    n = len(text)
    m = len(pattern)
    comparisons = 0
    
    if m == 0:
        return 0, 0
    
    h = 1
    for i in range(m - 1):
        h = (h * d) % q
    
    p_hash = 0
    t_hash = 0
    
    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q
    
    for i in range(n - m + 1):
        comparisons += 1
        if p_hash == t_hash:
            j = 0
            while j < m:
                comparisons += 1
                if text[i + j] != pattern[j]:
                    break
                j += 1
            
            if j == m:
                return i, comparisons
        
        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            if t_hash < 0:
                t_hash = t_hash + q
    
    return -1, comparisons

def read_files_from_links():
    import urllib.request
    import ssl
    
    # Створюємо SSL контекст, який ігнорує перевірку сертифікатів
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Прямі посилання для завантаження з Google Drive
    direct_links = [
        "https://drive.google.com/uc?export=download&id=18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh",
        "https://drive.google.com/uc?export=download&id=18BfXyQcmuinEI_8KDSnQm4bLx6yIFS_w"
    ]
    
    filenames = ["article1.txt", "article2.txt"]
    
    print("Завантаження файлів з Google Drive...")
    
    for i, (link, filename) in enumerate(zip(direct_links, filenames)):
        try:
            # Створюємо request з SSL контекстом
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
            urllib.request.install_opener(opener)
            
            urllib.request.urlretrieve(link, filename)
            print(f"Файл {filename} завантажено")
            
        except Exception as e:
            print(f"Помилка завантаження {filename}: {e}")
            print("Перевірте посилання та з'єднання з інтернетом")

def test_algorithms():
    algorithms = [
        ("Боєра-Мура", boyer_moore_search),
        ("Кнута-Морріса-Пратта", kmp_search),
        ("Рабіна-Карпа", rabin_karp_search)
    ]
    
    read_files_from_links()
    
    files = [
        ("article1.txt", "Стаття 1"),
        ("article2.txt", "Стаття 2")
    ]
    
    existing_patterns = ["алгоритм", "структур", "даних", "пошук"]
    non_existing_patterns = ["відсутній", "неіснуючий"]
    
    print("ПОРІВНЯННЯ ЕФЕКТИВНОСТІ АЛГОРИТМІВ ПОШУКУ ПІДРЯДКА")
    print("Алгоритми: Боєра-Мура, Кнута-Морріса-Пратта, Рабіна-Карпа")
    print("=" * 80)
    
    all_results = {}
    
    for filename, file_desc in files:
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        
        print(f"\n{file_desc}")
        print(f"Розмір тексту: {len(text)} символів")
        print("-" * 80)
        
        file_results = {}
        
        test_patterns = existing_patterns + non_existing_patterns
        
        for pattern in test_patterns:
            print(f"\nПошук підрядка: '{pattern}'")
            print(f"{'Алгоритм':<25} {'Час (мкс)':<15} {'Порівняння':<15} {'Результат'}")
            print("-" * 80)
            
            pattern_results = {}
            
            for alg_name, alg_func in algorithms:
                times = []
                
                for _ in range(100):
                    start_time = timeit.default_timer()
                    position, comparisons = alg_func(text, pattern)
                    end_time = timeit.default_timer()
                    times.append((end_time - start_time) * 1000000)
                
                avg_time = sum(times) / len(times)
                result = f"Позиція {position}" if position != -1 else "Не знайдено"
                
                pattern_results[alg_name] = {
                    'time': avg_time,
                    'comparisons': comparisons,
                    'position': position
                }
                
                print(f"{alg_name:<25} {avg_time:<15.2f} {comparisons:<15} {result}")
            
            fastest = min(pattern_results.items(), key=lambda x: x[1]['time'])
            most_efficient = min(pattern_results.items(), key=lambda x: x[1]['comparisons'])
            
            print(f"\nНайшвидший: {fastest[0]} ({fastest[1]['time']:.2f} мкс)")
            print(f"Найменше порівнянь: {most_efficient[0]} ({most_efficient[1]['comparisons']} порівнянь)")
            
            file_results[pattern] = pattern_results
        
        all_results[file_desc] = file_results
    
    return all_results

def analyze_results(results):
    print("\n" + "=" * 80)
    print("ЗАГАЛЬНИЙ АНАЛІЗ")
    print("=" * 80)
    
    algorithms = ["Боєра-Мура", "Кнута-Морріса-Пратта", "Рабіна-Карпа"]
    
    total_time = {alg: 0 for alg in algorithms}
    total_comparisons = {alg: 0 for alg in algorithms}
    wins_time = {alg: 0 for alg in algorithms}
    wins_comparisons = {alg: 0 for alg in algorithms}
    test_count = 0
    
    for file_name, file_results in results.items():
        for pattern, pattern_results in file_results.items():
            test_count += 1
            
            for alg_name in algorithms:
                total_time[alg_name] += pattern_results[alg_name]['time']
                total_comparisons[alg_name] += pattern_results[alg_name]['comparisons']
            
            fastest = min(pattern_results.items(), key=lambda x: x[1]['time'])
            most_efficient = min(pattern_results.items(), key=lambda x: x[1]['comparisons'])
            
            wins_time[fastest[0]] += 1
            wins_comparisons[most_efficient[0]] += 1
    
    print("Середні показники:")
    print(f"{'Алгоритм':<25} {'Час (мкс)':<15} {'Порівняння':<15}")
    print("-" * 55)
    
    for alg in algorithms:
        avg_time = total_time[alg] / test_count
        avg_comparisons = total_comparisons[alg] / test_count
        print(f"{alg:<25} {avg_time:<15.2f} {avg_comparisons:<15.1f}")
    
    print(f"\nКількість перемог за швидкістю:")
    for alg in algorithms:
        print(f"{alg}: {wins_time[alg]} з {test_count}")
    
    print(f"\nКількість перемог за ефективністю:")
    for alg in algorithms:
        print(f"{alg}: {wins_comparisons[alg]} з {test_count}")
    
    best_overall_time = min(total_time.items(), key=lambda x: x[1])
    best_overall_comparisons = min(total_comparisons.items(), key=lambda x: x[1])
    
    print(f"\nНайшвидший загалом: {best_overall_time[0]}")
    print(f"Найефективніший загалом: {best_overall_comparisons[0]}")

def generate_markdown_report(results):
    markdown_content = """# Порівняння ефективності алгоритмів пошуку підрядка

## Досліджені алгоритми
- **Боєра-Мура** - використовує таблицю поганих символів
- **Кнута-Морріса-Пратта (KMP)** - використовує префікс-функцію  
- **Рабіна-Карпа** - використовує хешування

## Результати тестування

"""
    
    algorithms = ["Боєра-Мура", "Кнута-Морріса-Пратта", "Рабіна-Карпа"]
    
    for file_name, file_results in results.items():
        markdown_content += f"### {file_name}\n\n"
        
        for pattern, pattern_results in file_results.items():
            markdown_content += f"#### Пошук підрядка: '{pattern}'\n\n"
            markdown_content += "| Алгоритм | Час (мкс) | Порівняння | Результат |\n"
            markdown_content += "|----------|-----------|------------|----------|\n"
            
            for alg_name in algorithms:
                if alg_name in pattern_results:
                    result_data = pattern_results[alg_name]
                    result = f"Позиція {result_data['position']}" if result_data['position'] != -1 else "Не знайдено"
                    markdown_content += f"| {alg_name} | {result_data['time']:.2f} | {result_data['comparisons']} | {result} |\n"
            
            if pattern_results:
                fastest = min(pattern_results.items(), key=lambda x: x[1]['time'])
                most_efficient = min(pattern_results.items(), key=lambda x: x[1]['comparisons'])
                
                markdown_content += f"\n**Найшвидший**: {fastest[0]} ({fastest[1]['time']:.2f} мкс)\n"
                markdown_content += f"**Найефективніший**: {most_efficient[0]} ({most_efficient[1]['comparisons']} порівнянь)\n\n"
    
    # Загальний аналіз
    markdown_content += "## Загальний аналіз\n\n"
    
    total_time = {alg: 0 for alg in algorithms}
    total_comparisons = {alg: 0 for alg in algorithms}
    wins_time = {alg: 0 for alg in algorithms}
    wins_comparisons = {alg: 0 for alg in algorithms}
    test_count = 0
    
    for file_name, file_results in results.items():
        for pattern, pattern_results in file_results.items():
            test_count += 1
            
            for alg_name in algorithms:
                if alg_name in pattern_results:
                    total_time[alg_name] += pattern_results[alg_name]['time']
                    total_comparisons[alg_name] += pattern_results[alg_name]['comparisons']
            
            fastest = min(pattern_results.items(), key=lambda x: x[1]['time'])
            most_efficient = min(pattern_results.items(), key=lambda x: x[1]['comparisons'])
            
            wins_time[fastest[0]] += 1
            wins_comparisons[most_efficient[0]] += 1
    
    markdown_content += "### Середні показники\n\n"
    markdown_content += "| Алгоритм | Час (мкс) | Порівняння |\n"
    markdown_content += "|----------|-----------|------------|\n"
    
    for alg in algorithms:
        if test_count > 0:
            avg_time = total_time[alg] / test_count
            avg_comparisons = total_comparisons[alg] / test_count
            markdown_content += f"| {alg} | {avg_time:.2f} | {avg_comparisons:.1f} |\n"
    
    markdown_content += f"\n### Статистика перемог\n\n"
    markdown_content += "| Алгоритм | Перемоги за швидкістю | Перемоги за ефективністю |\n"
    markdown_content += "|----------|----------------------|-------------------------|\n"
    
    for alg in algorithms:
        markdown_content += f"| {alg} | {wins_time[alg]}/{test_count} | {wins_comparisons[alg]}/{test_count} |\n"
    
    best_overall_time = min(total_time.items(), key=lambda x: x[1])
    best_overall_comparisons = min(total_comparisons.items(), key=lambda x: x[1])
    
    markdown_content += f"\n**Найшвидший загалом**: {best_overall_time[0]}\n"
    markdown_content += f"**Найефективніший загалом**: {best_overall_comparisons[0]}\n\n"
    
    # Висновки
    markdown_content += """## Висновки

1. **Для коротких підрядків** всі алгоритми показують схожі результати
2. **Боєра-Мура** ефективний для довгих підрядків та великих алфавітів
3. **KMP** показує стабільні результати незалежно від вхідних даних  
4. **Рабіна-Карпа** підходить для пошуку кількох підрядків одночасно
5. **Час виконання** залежить від характеристик тексту та підрядка

## Рекомендації

- **Для загального використання**: KMP через стабільність
- **Для довгих шаблонів**: Боєра-Мура  
- **Для множинного пошуку**: Рабіна-Карпа
- **Для простих завдань**: будь-який з алгоритмів підійде
"""
    
    with open("algorithm_comparison_report.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print("Звіт збережено у файл: algorithm_comparison_report.md")

def main():
    results = test_algorithms()
    analyze_results(results)
    generate_markdown_report(results)
    
    print("\n" + "=" * 80)
    print("ВИСНОВКИ")
    print("=" * 80)
    print("1. Для коротких підрядків всі алгоритми показують схожі результати")
    print("2. Боєра-Мура ефективний для довгих підрядків та великих алфавітів")
    print("3. KMP показує стабільні результати незалежно від вхідних даних")
    print("4. Рабіна-Карпа підходить для пошуку кількох підрядків одночасно")
    print("5. Час виконання залежить від характеристик тексту та підрядка")

if __name__ == "__main__":
    main()