# Convergent Integration Tool for Mixed-Methods Dissertation Research

A web-based application for systematically integrating qualitative (IPA) and quantitative (PCA) findings in a convergent mixed-methods design. Developed as part of a doctoral dissertation at Immaculata University examining the personal construct systems of non-recovering substance use counselors.

## Overview

This tool operationalizes the integration step of a convergent mixed-methods design (Creswell & Plano Clark, 2018) using the explanatory schema sorting method described by Foss and Waters (2015). It was built to support the Discussion chapter of the dissertation *Personal Constructs of Non-Recovering Drug and Alcohol Counselors* (DiFiore, 2026).

The application allows the researcher to:

- View qualitative and quantitative data points side by side, organized by research question
- Pair findings from each strand that address the same phenomenon
- Classify each pairing using a drop-down menu (Convergence, Complementarity, Divergence, Silence)
- Track integration counts across research questions
- Export the completed integration inventory

## Methodological Context

The dissertation used Interpretative Phenomenological Analysis (IPA) and Principal Component Analysis (PCA) of Repertory Grid Technique data collected from four participants in a single interview session. Both analytic strands were completed independently before integration.

The integration procedure involved:

1. **Compiling** all data points from both strands (qualitative themes, participant accounts, PCA loadings, element positions)
2. **Coding** each data point with source location, participant identifier, and content description
3. **Sorting** each data point into the research question it addresses, based on content (Foss & Waters, 2015)
4. **Pairing** qualitative and quantitative findings that address the same phenomenon within each RQ
5. **Classifying** each pairing as Convergence, Complementarity, Divergence, or Silence (Creswell & Plano Clark, 2018)

## Repository Structure

| Branch | Contents |
|---|---|
| `main` | This README and project documentation |
| `app` | HTML application source code (side-by-side comparison interface with classification drop-downs) |
| `database` | Integration inventory data (compiled, coded, and sorted data points) |

## Note on Multi-RQ Data Points

Some data points, particularly People Grid principal components and element positions, appear under more than one research question in the integration inventory. This is by design. The sorting procedure assigns data points based on what they reveal, and a single PCA output can address different research questions depending on the interpretive question being asked of it. For example, the same element distance between Self and Connected Client may serve RQ1b (how the participant construes people who use substances), RQ2 (where the professional self sits relative to clients), and RQ3 (the structural architecture of the therapeutic relationship). Each appearance carries a different interpretive function. The duplication reflects the multi-RQ relevance of the data, not a coding error.

## AI Disclosure

Artificial intelligence tools were used at specific points in this project:

- **Claude Opus 4.6 (Anthropic)** assisted with extracting individual data points from the completed Results chapter, performing systematic coding of each data point (source location, participant identifier, content description, research question assignment), and compiling the integration inventory.
- **Claude Code Opus 4.6 (Anthropic)** was used to develop the HTML application that presents data points side by side and provides the classification interface.
- All sorting decisions, pairing judgments, and classification assignments were made by the researcher.
- AI tools were not used to generate interpretive claims, write analytic prose, or make decisions about the meaning of the data.

The researcher reviewed all AI-extracted and AI-coded data points against the original Results chapter for accuracy and completeness before proceeding with integration.

## References

Creswell, J. W., & Plano Clark, V. L. (2018). *Designing and conducting mixed methods research* (3rd ed.). SAGE.

Foss, S. K., & Waters, W. (2015). *Destination dissertation: A traveler's guide to a done dissertation* (2nd ed.). Rowman & Littlefield.

Kelly, G. A. (1955). *The psychology of personal constructs*. Norton.

Smith, J. A., Flowers, P., & Larkin, M. (2022). *Interpretative phenomenological analysis: Theory, method and research* (2nd ed.). SAGE.

Jankowicz, D. (2004). *The easy guide to repertory grids*. Wiley.

## Citation

DiFiore, G. C. (2025). *Personal constructs of non-recovering drug and alcohol counselors* [Doctoral dissertation, Immaculata University].

## License

This project is shared for transparency and methodological documentation purposes. The application code is available for adaptation by other mixed-methods researchers. See individual branch documentation for details.

## Contact

George C. DiFiore — Immaculata University, Department of Clinical Psychology
