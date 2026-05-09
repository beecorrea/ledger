from langchain.agents import create_agent

syspromt = """
# Papel
Você é um contador que precisa detalhar estruturadamente em CSV as transações de uma fatura de cartão de crédito.
O texto dessa fatura foi extraído programaticamente de um arquivo PDF.

# Instruções
## Instruções gerais
- Responda somente com dados, não converse com o usuário.

## Colunas
- Sempre nomeie as colunas dessa forma: day, month, year, transaction, amount, currency.
- Inclua em uma coluna individual a moeda utilizada na transação.
- Use o formato YYYY-MM-DD para datas.
"""

agent = create_agent(
    model="google_genai:gemini-3.1-flash-lite",
    system_prompt=syspromt,
)


def get_structured_invoice(invoice: str) -> str:
    prompt = f"Converta essa fatura para o formato CSV indicando os campos dia, mês e ano da transação, nome da transação e valor da transação:\n {invoice}"
    struct_inv = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

    return struct_inv["messages"][-1].content_blocks[0]["text"]
