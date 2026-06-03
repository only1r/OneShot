# AI-Powered Synthesizer
A high-performance, browser based software synthesizer featuring real time Digital Signal Processing (DSP) and an integrated AI Copilot powered by Google's Gemini 2.5 Flash.

[[DEMO](<Website Walkthrough.gif>)]

## Features

- **AI Sound Design Copilot**: Translates language descriptions into precise JSON schemas to dynamically automate synthesizer parameters.
- **Unison Detuning**: Calculates precise phase spread across multiple oscillators to simulate thick, wide supersaw analog textures.
- **Real-time Polyphonic DSPEngine:** Built entirely on the native HTML5 Web Audio API, featuring multi-voice allocation, ADSR volume envelopes, and dynamic Biquad lowpass filtering.

## System Architechture

- **Interface:** Vanilla Javascript
- **Backend:** Python 'FastAPI' server manages keys and ensures AI runs
- **AI:** Google's `Gemini 2.5 Flash` LLM uses strict system prompts to output mathematically valid JSON parameter states based on user text.

## Local Installation

### Prerequisites
- Python 3.8+
- A free [Google AI Studio API Key](https://aistudio.google.com/)

### Backend Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/only1r/OneShot.git](https://github.com/only1r/OneShot.git)
   cd ai-synth-copilot
##
Website link: https://only1r.github.io/OneShot/
