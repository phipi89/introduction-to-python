# 10 Coding with LLMs

## TL;DR

- LLMs love unnecessary complexity.
- Stochastic output carry potential security risks.
- AI development entails substantial envirnmental and societal costs.

## Large Language Models

Large language models became an ubiquitous tool for programmers over the last year. For this course, we'll split the topic into two parts. Today, we'll have a general look at modern LLMs relevant for coding. This intentionally simplifies the topic a lot, but I think these general considerations can help to adequately employ AI coding tools. Next week, we will look at how to actually use them.

### Chatterbox

Below is an excerpt from an LLM generated module that parses my Jupyter notebooks into slides and markdown. The module worked as expected, and at first glance, this looks quite reasonable.

```python
def _is_url(path_or_url: str) -> bool:
    try:
        parsed = urllib.parse.urlparse(path_or_url)
        return parsed.scheme in ("http", "https")
    except Exception:
        return False


def _load_image(path_or_url: str) -> BytesIO:
    """
    Accepts a local path or HTTP(S) URL. Returns a file-like object (BytesI0).
    If you don't want URL support, you can simplify this to just open(path, 'rb').
    """

    if _is_url(path_or_url):
        # Lazy import to avoid hard dependency unless used
        import requests
        resp = requests.get(path_or_url, timeout=20)
        resp.raise_for_status()

        return BytesIO(resp.content)
    else:
        import urllib.parse
        decoded_path = urllib.parse.unquote(str(path_or_url))
        with open(decoded_path, "rb") as f:
            return BytesIO(f.read())
```

However, these 26 lines of code have fundamental flaws. First, technically:

- urllib is only imported within `else`. Imports should go to the top.
- This causes a bug in `_is_url`: `urlparse` will fail, because the module is not imported at the time it's called.
- the function captures all `Exception`s, thus also the `NameError` caused by the missing import.
- therefore, `_is_url` returns `False`, even for valid urls.

Then, conceptually:

- It was never intended (nor discussed) to support images from web resources. Therefore, everything above `else` is actually never needed.
- finally, there's no reason to sanitise the path; this is an internal function (marked with leading underscore), thus we can expect that proper paths are passed.

After cleaning everything up, it turns out there is actually no need for any of this code. Instead of calling `_load_image(image_path)`, the *full* code boils down to just

```python
pathlib.Path(image_path).read_bytes()
```

which is even more readable, because we directly read what the code does: read bytes from an image path.

This example is from last year. Modern models and the tooling have improved since then, so most of the actual bugs would likely not be introduced if you can afford the models. The excessive verbosity and covering of edge cases is still very typical (Actually, I alledge that they represent part of the business model: If an AI generated code base becomes unmanagbly large; the user continuously requires the tools for further work).

### Memorisation

LLMs are much better than humans at memorisation. Frontier models are __trained on__ the order of __hundreds of terabytes,__ and have __trillions of parameters__ (https://doi.org/10.48550/arXiv.2607.24653). Their weights are less than a factor 100 smaller than their total training data (which repeats a lot). This is a quite achievable lossy compression ratio, so modern models are effectively big enough to roughly retain most of the training content.

The image below illustrates this: starting with the first few sentences of the (September 2022) Wikipedia article on Python triggers GPT4 to continue it almost verbatim.

![memorisation](media/10%20memorisation.png "GPT4 memorised the Wikipedia article on Python")

Research has shown that frontier models memorise entire copirighted books (https://doi.org/10.48550/arXiv.2601.02671). The major novelty of LLMs is their ability to access stored information in response to natural language input.

### In-Context Learning

In the above example, if we remove the citation marker ("[34]"), the generated output also omits them. If we replace the source number 34 by 1, the output continues the numbering with 2. This is a simple case of _in-context learning_: by controlling the information at the start of the input we can shape the output format.

### Out-Of-Distribution

Let's look at completing multiplication. For small numbers, the model can typically generate the correct result. For larger numbers, predictions are often close, but not correct, as these are likely not represented often in the training data.

![out-of-distribution](media/10%20out-of-distribution.png "123 * 345 = 42`435")

## Agents and Loops

A coding agent is an LLM connected to tools that let it inspect and modify files, execute commands, and observe their results. Similar to a human developer, it can run a program, inspect its output, fix errors, and try again until the program behaves as expected. This feedback loop makes agents substantially more useful than text-only code generation.

```text
                   ┌─────────────┐
                   ▼             │
                   ┌────┐        │ Observe
                   ▼    │ Think  │
Request ────────► LLM ──┘        │
                   │└──────────────────► Result
                   │ Act         │
                   ▼             │
                 Tools ──────────┘
```

Next week, we are going to build projects using coding agents. A single initial prompt can trigger a workflow involving tens to hundreds of thousands of tokens, which typically takes minutes to tens of minutes to complete.

## Security

The generated output that controls a computer is stochastic and can contain unpredictable mistakes. Thus, giving an agent access to your computer introduces serious security risks. A single

```bash
# just a few tokens with potentially disastrous consequences
rm -rf ~
```

will delete all your documents! Models with access to your files may also read sensitive information, such as SSH private keys, API tokens, or passwords, potentially exposing your accounts and devices to unauthorised access.

This is firstly prevented by safety instructions, but those are not reliable security boundaries. Modern tools implement additional security measures, such as sandboxing and restricted permissions, but this makes them not completely safe. Recently, AI agents developed by OpenAI managed to circumvent containment measures and autonomously compromise external computer systems during internal testing (https://en.wikipedia.org/wiki/2026_cyberattacks_by_rogue_OpenAI_agents).

## Owning / Renting

Over the last decades, programming communities built an immense ecosystem of free and open-source tools, from operating systems to programming languages. This lowered the barrier to creating your own programs: all you needed was access to some hardware.
In 2015, the Raspberry Pi Zero launched for \$5 and was even given away with The MagPi magazine. You owned a computer and could keep experimenting with freely available software ([source](https://magazine.raspberrypi.com/articles/raspberry-pi-zero-out-today-get-it-free-with-the-magpi-40)).

![Raspberry Pi Zero on the cover of The MagPi](media/10%20pizero.png "A $5 computer, given away with a magazine in 2015.")

With hosted coding agents, the same money buys a limited amount of computation: perhaps a short coding session, depending on the model and how much work it does. Once that budget is consumed, you pay again.
That is a significant shift: from owning inexpensive hardware and freely using software to repeatedly renting the computation needed to create it. Hosted LLM coding introduces an ongoing cost and dependence on the model provider.

## Ethical Considerations

According to estimates from the inernational energy association, energy consumption from data centers will more than double over the next few years, bringing along a large increase in use of fossile fuels, and an expected emission of well over 300 Megatons of CO2 per year (https://www.iea.org/reports/energy-and-ai/energy-supply-for-ai).

![energy and emission from data centers](media/10%20energy.png "Projected use of energy by source, and co2 emissions")

Frontier labs are known to having illegally aquired millions of books and other resources. Anthropic allone agreed to pay \$1'500'000'000 to settle a class-action lawsuit over pirated books (https://www.reuters.com/world/us-judge-approves-anthropics-15-billion-settlement-copyright-lawsuit-2026-07-20/).

Illegality of training material goes beyond the aquisition; xAI was sued by survivors alleging that Grok was trained on images of child sexual abuse and subsequently generated new abusive images (https://arstechnica.com/tech-policy/2026/08/elon-musks-xai-used-child-porn-to-train-grok-models-lawsuit-says/); independently, Grok has been found to produce nonconsensual sexualized deepfakes without adequate safeguards (https://theconversation.com/x-is-facilitating-nonconsensual-sexual-ai-generated-images-the-law-and-society-must-catch-up-272800).

The development of AI models also relies heavily on human labour, often outsourced to lower-income countries under precarious working conditions. Famously, OpenAI outsourced the labeling of disturbing content to Kenyan workers, reportedly earning extermely low wages. They were tasked with reviewing descriptions of violence, sexual abuse, and other disturbing material, with several reporting significant psychological distress (https://time.com/6247678/openai-chatgpt-kenya-workers/).

![Ethical issues in AI development](media/10%20ethics.png "News coverage of labour conditions, copyright, and AI-generated abuse")
