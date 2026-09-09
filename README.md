# QuPCG: Quantum Convolutional Neural Network for Detecting Abnormal Patterns in PCG Signals

---

**For the full paper and technical details, please refer to:**

- Y. Torabi, S. Shirani, and J. P. Reilly, *“QuPCG: Quantum Convolutional Neural Network for Detecting Abnormal Patterns in PCG Signals,”* 2025.

DOI: [https://arxiv.org/abs/2511.02140](https://arxiv.org/abs/2511.02140)

## Abstract

Early identification of abnormal physiological patterns is essential for the timely detection of cardiac disease. This work introduces a hybrid quantum–classical convolutional neural network (QCNN) designed to classify S3 and murmur abnormalities in heart sound signals.

The approach transforms one-dimensional phonocardiogram (PCG) signals into compact two-dimensional images through wavelet feature extraction and adaptive compression. The cardiac sound patterns are progressively compressed into an 8-value representation so that only 8 qubits are needed for the quantum stage. The QCNN then extracts hierarchical features through successive quantum convolution and pooling layers.

Preliminary results on the HLS-CMDS dataset demonstrate **93.33% classification accuracy on the test set**, showing the potential of compact quantum–classical models for biomedical signal processing.

<img src="fig1.png" alt="Overview of the proposed hybrid quantum-classical model" width="500"/>

---

## Method

The proposed method consists of a classical preprocessing stage followed by a quantum processing stage.

The classical stage transforms PCG signals into compact quantum-ready representations using:

- Continuous Wavelet Transform (CWT)
- Complex Morlet wavelet
- Downsampling
- Binarization
- Feature compression

The resulting representation contains **8 values**, which are encoded into **8 qubits**. The quantum stage consists of three successive quantum convolution and pooling stages, followed by measurement for classification.

The model classifies abnormal heart sound patterns into two categories:

- **S3**
- **Murmur**

<img src="fig3.png" alt="Progressive compression of wavelet scalograms for quantum encoding" width="500"/>

---

## Dataset

The experiments use the **HLS-CMDS** heart and lung sound dataset.

- 535 recordings
- CAE Juno clinical manikin
- 3M Littmann CORE Digital Stethoscope
- Sampling rate: 22,050 Hz
- Recording duration: 15 seconds
- Normal and abnormal cardiac sounds
- Classification task: S3 vs. murmur

The dataset is publicly available:

- https://github.com/Torabiy/HLS-CMDS

---

## Implementation

The quantum circuit was implemented using:

- Qiskit 0.45
- AerSimulator
- 8 qubits
- COBYLA optimizer
- Learning rate: 0.01
- Batch size: 16
- 200 training epochs
- 1000 epochs for the enhanced W-QuPCG⁺ model
- NVIDIA GeForce RTX 4090 GPU with 24 GB memory

---

## Results

Four different QCNN configurations were evaluated:

| Method | Accuracy (Train) | Accuracy (Test) | Loss (Train) | Loss (Test) |
|---|---:|---:|---:|---:|
| I-QuPCG | 51.06 ± 2.3% | 47.62 ± 2.8% | 1.00 ± 0.25 | 1.10 ± 0.54 |
| M-QuPCG | 74.29 ± 5.2% | 53.33 ± 4.0% | 0.80 ± 0.13 | 0.91 ± 0.25 |
| W-QuPCG | 91.43 ± 2.9% | 80.00 ± 6.1% | 0.69 ± 0.12 | 0.73 ± 0.03 |
| **W-QuPCG⁺** | **97.14 ± 4.6%** | **93.33 ± 2.9%** | **0.42 ± 0.62** | **0.45 ± 0.12** |

W-QuPCG⁺ achieved the best overall performance, demonstrating that wavelet-based time–frequency representations combined with compact quantum encoding can effectively support PCG classification.

---

## Source Code

The Python implementation is publicly available:

- https://github.com/Torabiy/QuPCG

---

## Citation

If you use this code or research in your work, please cite:

- Y. Torabi, S. Shirani, and J. P. Reilly, *“QuPCG: Quantum Convolutional Neural Network for Detecting Abnormal Patterns in PCG Signals,”* 2025.

---

## License

© 2025 by Yasaman Torabi. All rights reserved.
