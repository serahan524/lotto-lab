from lotto_lab.fetcher import fetch_html
from lotto_lab.pipeline import process_draws
from lotto_lab.orchestration import save_draws
from lotto_lab.storage.sqlite_storage import initialize_database



def collect_history(db_path, months):
    successful_months = []
    partial_success_months = []
    failed_months = []

    initialize_database(db_path)

    for back in range(months):
        url = f"https://www.wclc.com/western-649-extra.htm?back={back}"

        try:
            html = fetch_html(url)

            result = process_draws(html)
            valid_count = len(result["valid_draws"])
            error_count = len(result["errors"])

            status = determine_status(valid_count, error_count)

            storage_status = None

            if status != "failed":
                storage_result = save_draws(db_path, result["valid_draws"])
                print(f"back={back}, storage={storage_result}")

                storage_status = determine_storage_status(storage_result)

            if status == "success" and storage_status == "success":
                successful_months.append(back)
            elif status == "partial_success" and storage_status == "success":
                partial_success_months.append(back)
            else:
                failed_months.append({
                    "back": back,
                    "processing_status": status,
                    "storage_status": storage_status
                })

        except Exception as error:
            print(f"Failed back={back}: {error}")
            
            failed_months.append({
                "back": back,
                "reason": str(error)
            })

    return {
        "successful_months": successful_months,
        "partial_success_months": partial_success_months,
        "failed_months": failed_months,
    }


def determine_status(valid_count, error_count):

    if valid_count == 0: 
        return "failed"

    if error_count == 0: 
        return "success"
    
    return "partial_success"


def determine_storage_status(storage_result):

    if storage_result["conflict"] == 0 and storage_result["error"] == 0:
        return "success"
    
    return "failed" 