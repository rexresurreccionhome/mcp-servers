# Types of Data in ML

## 1. Numerical Data
- **Continuous**: Measurements that can take any value within a range (e.g., temperature, height, weight, price)
- **Discrete**: Countable values (e.g., number of items, age in years, population count)

## 2. Categorical Data
- **Nominal**: Categories without inherent order (e.g., colors, gender, country, product types)
- **Ordinal**: Categories with a meaningful order (e.g., education level, satisfaction ratings: low/medium/high)

## 3. Text Data
- Unstructured text like documents, reviews, emails, social media posts
- Requires preprocessing techniques:
  - Tokenization
  - Vectorization (Bag of Words, TF-IDF, word embeddings)
  - Stemming/Lemmatization

## 4. Time Series Data
- Sequential data points indexed in time order
- Examples: stock prices, sensor readings, weather data, sales forecasts
- Temporal dependencies are important

### 4a. Streaming Data (Real-time Data)
- Continuous flow of data generated in real-time
- Requires online/incremental learning algorithms
- Examples: live sensor feeds, clickstream data, social media feeds, IoT device data
- Key difference: data arrives continuously and may not be stored permanently
- Often processed using sliding windows or mini-batches

## 5. Image Data
- Visual data represented as pixel arrays
- Can be grayscale (single channel) or color (RGB - 3 channels)
- Examples: photographs, medical scans, satellite imagery

## 6. Audio Data
- Sound waves represented as digital signals
- Used in speech recognition, music analysis, sound classification
- Often processed as spectrograms or waveforms

## 7. Graph/Network Data
- Relationships between entities represented as nodes and edges
- Examples: social networks, molecular structures, recommendation systems, knowledge graphs

## 8. Video Data
- Sequence of image frames over time
- Combines spatial and temporal information
- Used in action recognition, video surveillance, autonomous vehicles
