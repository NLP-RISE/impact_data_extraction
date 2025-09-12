from outformer import Jsonformer, highlight_values
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize model and tokenizer
model_name = "mistralai/Mixtral-8x7B-v0.1"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="balanced",
    top_k=10,
    do_sample=True,
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create Jsonformer instance
jsonformer = Jsonformer(model, tokenizer, max_tokens_string=1000, debug=False)

# Define your JSON schema
json_schema = {
    "type": "object",
    "properties": {
        "shoes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "brand": {
                        "type": "string",
                        "description": "Brand of the product",
                    },
                    "model": {
                        "type": "string",
                        "description": "Model of the product",
                    },
                    "product_type": {
                        "type": "string",
                        "description": "Type of the product",
                    },
                    "gender": {
                        "type": "string",
                        "enum": ["Female", "Male", "Unisex"],
                    },
                    "color": {
                        "type": "string",
                        "description": "Color of the product if specified, otherwise return 'Unknown'",
                    },
                    "material": {
                        "type": "string",
                        "description": "Material of the product if specified, otherwise return 'Unknown'",
                    },
                    "features": {
                        "type": "array",
                        "minItems": 3,
                        "items": {
                            "type": "string",
                            "description": "Features of the product that may be relevant for the customer. Extract as much as possible.",
                        },
                    },
                },
            },
        }
    },
}

ad = """
### Ad 1: The Performance Runner (Targeting Athletes & Fitness Enthusiasts)

**Headline:** Defy Your Limits. Feel the AeroWeave Difference.

**Visual:** A dynamic, slow-motion shot of a runner on a misty morning trail, their foot striking the ground perfectly. The shoe flexes, showcasing its sole technology.

**Body Copy:**
> Every step is a choice between hitting the wall and breaking through it. Introducing the new **Nexus AeroWeave**, engineered for the runner who refuses to quit.
>
> With our revolutionary **CloudCell midsole**, you get 30% more energy return than standard foam. The **AeroWeave mesh upper** provides breathable, adaptive support that moves with your foot, not against it.
>
> **Don't just run. Fly.**
>
> **#TakeFlight | Shop the Nexus AeroWeave Collection**

---

### Ad 2: The Urban Everyday Sneaker (Targeting Fashion-Conscious Millennials/Gen Z)

**Headline:** Your City. Your Style. Your Go-To.

**Visual:** A clean, stylish flatlay of the sneaker on a concrete step, paired with interesting socks and the cuff of well-fitted jeans. The overall aesthetic is minimalist and urban.

**Body Copy:**
> Found: The one sneaker that literally goes with everything. Meet the **Metro Pivot**, the effortlessly cool essential for your wardrobe.
>
> Crafted from premium suede and recycled materials, its timeless low-top design transitions from day to night, from brunch to the park. Comfortable enough to conquer your daily 10,000 steps without sacrificing an ounce of style.
>
> **Get Yours. Define Your Everyday.**
>
> **#MetroPivot #EverydayEssential | Available Now**

---

### Ad 3: The Professional Comfort Shoe (Targeting Working Professionals)

**Headline:** Conference Room to Commute. Mastered.

**Visual:** A sharp-dressed professional walking confidently through a city street. The focus is on their sharp outfit, with a quick, stylish cut to the shoe itself as they step off a curb.

**Body Copy:**
> You command the boardroom. Shouldn't your shoes keep up? Introducing **OxfordCraft: The Executive Series**.
>
> We've reimagined the classic dress shoe with a secret: a **cloud-comfort insole** and flexible sole designed for all-day support. Finally, sophisticated style doesn't come at the cost of comfort. Look powerful *and* feel powerful from your first meeting to your last.
>
> **Step Into Success. Comfortably.**
>
> **#Workleisure #OxfordCraft | Shop Professional Comfort**
"""


prompt = f"""
Extract a list of shoes and their key items from the ads below.

Ads:
---------
{ad}
--------
"""

print("..... temp 0")
# Generate structured output
generated_data = jsonformer.generate(
    schema=json_schema, prompt=prompt, temperature=0.0, max_attempts=10
)

# Highlight generated values
highlight_values(generated_data)

print("..... temp 0.25")

# Generate structured output
generated_data = jsonformer.generate(
    schema=json_schema, prompt=prompt, temperature=0.25, max_attempts=10
)

# Highlight generated values
highlight_values(generated_data)

print("..... temp 0.75")


# Generate structured output
generated_data = jsonformer.generate(
    schema=json_schema, prompt=prompt,temperature=0.75, max_attempts=10
)

# Highlight generated values
highlight_values(generated_data)
