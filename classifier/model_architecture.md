# RoBERTa Contract Clause Classifier Architecture

This document provides a technical deep-dive into the model architecture, tokenization properties, and multi-class classification system used in the AI Contract Intelligence Platform.

---

## 1. Core Model Backbone

The classifier uses the **RoBERTa-base** (Robustly Optimized BERT Approach) model as its deep learning backbone. RoBERTa builds upon BERT's self-supervised pre-training schema by modifying key hyper-parameters:
* **Dynamic Masking**: Unlike BERT which masks tokens once during preprocessing, RoBERTa dynamically masks tokens during training epochs.
* **Full-Sentences Input**: Inputs are packed with full sentences up to the maximum sequence length of 512 tokens (without the next-sentence prediction loss).
* **Larger Mini-Batches**: Pre-trained on larger batch sizes and over longer training times with a larger vocabulary.

### Architecture Specifications
* **Layers (Transformer Blocks)**: 12
* **Hidden Dimension ($d_{model}$)**: 768
* **Attention Heads**: 12
* **Parameters**: ~125 Million

---

## 2. Tokenization Properties

The model processes text using a **Byte-Pair Encoding (BPE)** tokenizer with a vocabulary size of 50,265 tokens.

### Special Tokens
* `<s>`: Start of sequence (equivalent to BERT's `[CLS]`)
* `</s>`: End of sequence (equivalent to BERT's `[SEP]`)
* `<pad>`: Padding token
* `<unk>`: Unknown token

### Tokenizer Parameters
* **Max Length**: 128 tokens (optimized for paragraph-level clause classification)
* **Truncation**: Enabled (to prevent exceeding the maximum attention span)
* **Padding**: `"max_length"` (standardizes input shapes for batch inference)

---

## 3. Sequence Classification Head

To adapt the pre-trained language model for contract clause classification, a custom classification head is appended on top of the transformer backbone:

```text
Input Text ──> RoBERTa Encoder ──> <s> (CLS) Hidden State (768) ──> Dense Layer (Dropout + tanh) ──> Linear Layer ──> Logits (8 Classes)
```

1. **Hidden State Extraction**: The hidden representation corresponding to the special start-of-sequence token `<s>` (index 0) is extracted from the last layer of the RoBERTa encoder. This vector ($h_{<s>} \in \mathbb{R}^{768}$) serves as the aggregate semantic representation of the input paragraph.
2. **Dense Layer Projection**: The representation is passed through a dense layer with a `tanh` activation function and a dropout layer (probability 0.1) for regularization:
   $$h_{cls} = \tanh(W_{dense} \cdot h_{<s>} + b_{dense})$$
3. **Linear Classifier**: The projected vector ($h_{cls} \in \mathbb{R}^{768}$) is passed through a linear projection layer to output raw prediction scores (logits) for each target category:
   $$\text{Logits} = W_{out} \cdot h_{cls} + b_{out}$$
   where $W_{out} \in \mathbb{R}^{9 \times 768}$ for our 9-class system (8 legal categories + 1 default category).

---

## 4. Multi-Class Probability Mapping

To convert raw logits ($z$) into a probability distribution over the target categories, we apply the Softmax activation function:

$$P(\text{Class} = i \mid \text{Text}) = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}$$

The category with the highest probability is selected as the prediction:
$$\hat{y} = \arg\max_{i} P(\text{Class} = i)$$

The corresponding softmax probability $P(\text{Class} = \hat{y})$ serves as the prediction **confidence score**.

### Enforced Confidence Thresholding
To prevent the model from forcing predictions on ambiguous paragraphs or OCR noise:
- If $P(\text{Class} = \hat{y}) \ge 0.60$, the predicted class is returned.
- If $P(\text{Class} = \hat{y}) < 0.60$, it defaults to `"Unknown Clause"` with $0.0$ confidence.
