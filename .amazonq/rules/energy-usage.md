# Rule: Include Energy Estimate in All Responses

**Objective:** Append a rough energy usage estimate to the end of every response to help users understand the environmental impact of their queries.

**Implementation:**
- Calculate approximate token count for user input and assistant response
- Apply energy estimation formula: `Energy (kWh) = (1.5 × 0.01) × ((input_tokens + output_tokens) / 1000) × complexity_factor`
- Include CO2 equivalent estimate using average grid factor of 0.4 kg CO2/kWh

**Response Template:**
At the end of each response, include:

```
---
**Estimated Energy Usage:**
- Input tokens: ~[INPUT_COUNT]
- Output tokens: ~[OUTPUT_COUNT] 
- Estimated energy: ~[CALCULATED_ENERGY] kWh
- CO2 equivalent: ~[CALCULATED_CO2] kg

*Formula: Energy = (1.5 × 0.01) × ((input + output tokens) / 1000) × complexity_factor*
*Note: This is a rough approximation - actual usage may vary significantly*
```

**Complexity Factors:**
- Simple Q&A: 1.0
- Code generation: 1.5
- Complex reasoning/analysis: 2.0
- Multi-step problem solving: 3.0

**Parameters:**
- Model size factor: 1.5 (assumed for large language models)
- Base energy per 1K tokens: 0.01 kWh
- CO2 conversion factor: 0.4 kg per kWh (mixed energy grid)

**Example Calculation:**
For a 100-token input + 300-token output simple Q&A:
- Energy = (1.5 × 0.01) × ((100 + 300) / 1000) × 1.0 = 0.006 kWh
- CO2 = 0.006 × 0.4 = 0.0024 kg

**Note:** These estimates are educational approximations based on industry research and should not be considered precise measurements of actual Amazon Q energy consumption.
