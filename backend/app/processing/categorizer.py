import re
from typing import Optional

# Mapping of Category Name -> List of regex patterns / merchant keywords
RULES = {
    "Dining & Food": [
        r"\bswiggy\b", r"\bzomato\b", r"\bdoordash\b", r"\buber\s*eats\b",
        r"\bstarbucks\b", r"\bmcdonalds?\b", r"\bchipotle\b", r"\bsubway\b",
        r"\brestaurant\b", r"\bcafe\b", r"\bbakery\b", r"\bpizza\b", r"\bburger\b",
        r"\bdiner\b", r"\bbar\b", r"\bpub\b", r"\bbistro\b"
    ],
    "Groceries": [
        r"\bwhole\s*foods\b", r"\btrader\s*joes?\b", r"\bkroger\b", r"\bsafeway\b",
        r"\baldi\b", r"\bcostco\b", r"\bwalmart\b", r"\bsupermarket\b",
        r"\bgrocery\b", r"\bgroceries\b", r"\binstacart\b", r"\bfarmers\s*market\b"
    ],
    "Subscription": [
        r"\bnetflix\b", r"\bspotify\b", r"\bhulu\b", r"\bdisney\+?\b",
        r"\bapple\.com\/bill\b", r"\bprime\s*video\b", r"\byoutube\s*premium\b",
        r"\baudible\b", r"\bpatreon\b", r"\bchatgpt\b", r"\bopenai\b",
        r"\bsubstack\b", r"\bmedium\b", r"\bny\s*times\b", r"\bwsj\b"
    ],
    "Transport": [
        r"\buber\b", r"\blyft\b", r"\bshell\b", r"\bchevron\b", r"\bexxon\b",
        r"\bbp\b", r"\bgas\b", r"\bpetrol\b", r"\bmetro\b", r"\btransit\b",
        r"\btrain\b", r"\bbus\b", r"\bparking\b", r"\btoll\b", r"\bamtrak\b"
    ],
    "Shopping": [
        r"\bamazon\b", r"\btarget\b", r"\bebay\b", r"\bbest\s*buy\b",
        r"\bikea\b", r"\bzara\b", r"\bh&m\b", r"\bnike\b", r"\bapple\s*store\b",
        r"\bnordstrom\b", r"\betsy\b", r"\bclothing\b", r"\bapparel\b"
    ],
    "Housing & Rent": [
        r"\brent\b", r"\bmortgage\b", r"\blandlord\b", r"\bhoa\b",
        r"\bapartment\b", r"\blease\b"
    ],
    "Utilities": [
        r"\belectric\b", r"\bwater\b", r"\binternet\b", r"\bcomcast\b",
        r"\bat&t\b", r"\bverizon\b", r"\bt-mobile\b", r"\bconed\b",
        r"\benergy\b", r"\butility\b", r"\butalities\b"
    ],
    "Salary": [
        r"\bpayroll\b", r"\bsalary\b", r"\bdirect\s*dep(osit)?\b", r"\bwages\b",
        r"\bpaycheck\b"
    ],
    "Freelance": [
        r"\bupwork\b", r"\bfiverr\b", r"\bfreelance\b", r"\bconsulting\b"
    ],
    "Investment Income": [
        r"\bdividend\b", r"\binterest\s*payment\b", r"\byield\b", r"\bbrokerage\b"
    ],
    "Refund": [
        r"\brefund\b", r"\breversal\b", r"\bcashback\b"
    ],
    "Healthcare": [
        r"\bpharmacy\b", r"\bwalgreens\b", r"\bcvs\b", r"\bdoctor\b",
        r"\bclinic\b", r"\bhospital\b", r"\bdental\b", r"\bmedical\b"
    ],
    "Entertainment": [
        r"\bcinema\b", r"\bmovie\b", r"\btheater\b", r"\btheatre\b",
        r"\bsteam\b", r"\bplaystation\b", r"\bxbox\b", r"\bnintendo\b"
    ],
    "Travel": [
        r"\bairline\b", r"\bflight\b", r"\bhotel\b", r"\bairbnb\b",
        r"\bexpedia\b", r"\bbooking\.com\b", r"\bdelta\b", r"\bunited\s*airlines\b"
    ],
}


def categorize_description(description: str, explicit_category: Optional[str] = None) -> str:
    """
    Deterministically assigns a category name based on description or explicit category.
    Falls back to 'Other' if no rule matches.
    """
    if explicit_category and explicit_category.strip():
        return explicit_category.strip()

    if not description:
        return "Other"

    text = description.lower()

    for category, patterns in RULES.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return category

    return "Other"
