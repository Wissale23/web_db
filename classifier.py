def classify_page(url, text):

    u = url.lower()
    t = text.lower()

    if "admission" in u or "apply" in u or "deadline" in t:
        return "admissions"

    if "tuition" in u or "fees" in u or "financial" in u:
        return "tuition"

    if "academic" in u or "program" in u or "major" in u or "catalog" in u:
        return "academics"

    return "other"