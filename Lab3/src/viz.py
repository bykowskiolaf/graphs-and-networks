# Realizacja wyrysowywania stosu (Zad. 5) i wykresów przedziałów (Zad. 7)

def print_stack_state(stack):
    """Zadanie 5: Wyświetla stos w prostej grafice ASCII."""
    # Odfiltrowujemy flagi POST, żeby pokazać tylko wierzchołki tak jak na wykładzie
    display_items = [str(item[0]) for item in stack if not item[1]]
    if not display_items:
        print("Stos: [ PUSTY ]")
    else:
        print(f"Stos: [ {' | '.join(display_items)} ]")


def draw_intervals(pre, post, names=None):
    """
    Zadanie 7: Wykres przedziałów otwarcia/zamknięcia (pre/post).
    """
    n = len(pre)
    if names is None:
        names = [str(i) for i in range(n)]
        
    max_time = max(post)
    print("\n--- Wykres przedziałów otwarcia (Zadanie 7) ---")
    
    # Sortujemy po czasie otwarcia dla czytelności z góry na dół
    nodes_sorted = sorted(range(n), key=lambda x: pre[x])
    
    # Rysowanie osi czasu
    timeline = "Czas:   "
    for t in range(1, max_time + 1):
        timeline += f"{t:02d} "
    print(timeline)
    print("-" * len(timeline))
    
    for v in nodes_sorted:
        p_start = pre[v]
        p_end = post[v]
        
        # Formatowanie paska w ASCII
        prefix = "   " * (p_start - 1)
        length = p_end - p_start
        if length == 0:
            bar = "[x]"
        else:
            bar = "[" + "=" * (length * 3 - 2) + "]"
            
        print(f"Węzeł {names[v]:<2}: {prefix}{bar} ({p_start}/{p_end})")
    print("-" * len(timeline))