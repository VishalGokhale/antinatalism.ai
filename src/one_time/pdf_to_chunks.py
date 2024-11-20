# given a pdf file this function should extract all such that it is split into paragraphs

import pypdf
import tiktoken


def pdf_to_chunks(pdf_path: str) -> list[str]:
    text = ""
    with open(pdf_path, "rb") as f:
        pdf = pypdf.PdfReader(f)
        for page_num in range(pdf.get_num_pages()):
            page = pdf.get_page(page_num)
            text += page.extract_text()
    paras = text.split("\n")
    count = len(paras)
    chunks_1 = ["\n".join(paras[i:i + 5]) for i in range(0, count, 5)]
    chunks_2 = ["\n".join(paras[i:i + 5]) for i in range(3, count, 5)]
    chunks = chunks_1 + chunks_2
    return chunks


def save_chunks(chunks):
    import pickle
    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    import pandas as pd
    df = pd.DataFrame(chunks, columns=["chunks"])
    df.to_excel("chunks.xlsx")


if __name__ == '__main__':
    # pdf_path = r"C:\Users\gokhvis\Documents\antinatalism.ai\data\Benatar.pdf"
    pdf_path_ = r"C:\Users\gokhvis\Documents\antinatalism.ai\data\David_Benatar_-_Better_Never_to_Have_Been.pdf"
    chunks_ = pdf_to_chunks(pdf_path_)
    print(len(chunks_))
    save_chunks(chunks_)

    # encoder = tiktoken.encoding_for_model("text-embedding-3-small")
    #
    # encoded = [encoder.encode(x, disallowed_special=set()) for x in chunks]
    # encoded_lengths = [len(x) for x in encoded]
    # print("Total ", sum(encoded_lengths))
    # print("Max ", max(encoded_lengths))
