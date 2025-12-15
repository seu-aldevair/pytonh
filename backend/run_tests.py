"""Runner simples para executar os testes sem depender do pytest."""
from backend.tests import test_ai_engine


def main():
    funcs = [
        test_ai_engine.test_select_template_id_success,
        test_ai_engine.test_generate_proposal_success,
        test_ai_engine.test_select_template_invalid_response,
    ]
    for f in funcs:
        try:
            f()
            print(f"[PASS] {f.__name__}")
        except AssertionError as e:
            print(f"[FAIL] {f.__name__}: {e}")
        except Exception as e:
            print(f"[ERROR] {f.__name__}: {e}")


if __name__ == '__main__':
    main()
