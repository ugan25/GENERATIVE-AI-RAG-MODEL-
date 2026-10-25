from flask import Flask, render_template, request
from rag import PrintingRAG
from print_tool import calculate_print_order

app = Flask(__name__)
rag = PrintingRAG()

@app.route("/", methods=["GET", "POST"])
def index():
    estimate = None
    error = None
    answer = None
    question = ""

    if request.method == "POST":
        action = request.form.get("action", "estimate")

        if action == "estimate":
            try:
                pages = int(request.form.get("pages", ""))
                copies = int(request.form.get("copies", ""))
                colour_mode = request.form.get("colour_mode", "black_white")
                double_sided = request.form.get("double_sided") == "yes"
                binding_required = request.form.get("binding_required") == "yes"
                estimate = calculate_print_order(
                    pages_per_copy=pages,
                    copies=copies,
                    colour_mode=colour_mode,
                    double_sided=double_sided,
                    binding_required=binding_required,
                )
            except (ValueError, TypeError) as exc:
                error = str(exc)
        elif action == "ask":
            question = request.form.get("question", "").strip()
            if question:
                answer = rag.ask(question)
            else:
                error = "Please enter a question."

    return render_template(
        "index.html", estimate=estimate, error=error, answer=answer, question=question
    )

if __name__ == "__main__":
    app.run(debug=True)
