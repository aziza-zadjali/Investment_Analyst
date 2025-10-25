import React, { useState } from "react";
import { LLMHandler } from "./utils/llmHandler";
import { TemplateGenerator } from "./utils/templateGenerator";
import { WebScraper } from "./utils/webScraper";

interface AnalysisResults {
  companyName: string;
  industry: string;
  analystName: string;
  analysisDate: string;
  geographicMarkets: string[];
  analysisAreas: string[];
  marketSizeGrowth?: string;
  competitiveLandscape?: string;
  marketTrends?: string;
  swotAnalysis?: string;
  portersFiveForces?: string;
  customerSegmentation?: string;
  regulatoryEnvironment?: string;
}

export const MarketAnalysis: React.FC = () => {
  const [companyName, setCompanyName] = useState("");
  const [industry, setIndustry] = useState("");
  const [geographicFocus, setGeographicFocus] = useState<string[]>(["Global"]);
  const [companyWebsite, setCompanyWebsite] = useState("");
  const [analysisOptions, setAnalysisOptions] = useState<string[]>([
    "Market Size & Growth",
    "Competitive Landscape",
    "Market Trends & Drivers",
  ]);
  const [enableWebResearch, setEnableWebResearch] = useState(false);
  const [analysisResults, setAnalysisResults] = useState<AnalysisResults | null>(null);
  const [loading, setLoading] = useState(false);

  // Initialize handlers
  const llm = new LLMHandler();
  const templateGen = new TemplateGenerator();
  const webScraper = new WebScraper();

  const generateAnalysis = async () => {
    if (!companyName || !industry) {
      alert("⚠️ Please enter both company name and industry");
      return;
    }
    if (analysisOptions.length === 0) {
      alert("⚠️ Please select at least one analysis area");
      return;
    }

    setLoading(true);

    const results: AnalysisResults = {
      companyName,
      industry,
      analystName: "Regulus AI",
      analysisDate: new Date().toLocaleDateString(),
      geographicMarkets: geographicFocus,
      analysisAreas: analysisOptions,
    };

    try {
      // Optional Web Research
      if (enableWebResearch) {
        console.info("🌐 Gathering market data from web sources...");
        const searchQueries = [
          `${industry} market size analysis`,
          `${companyName} competitors analysis`,
          `${industry} market trends 2025`,
        ];
        for (const query of searchQueries) {
          console.info(`Searching: ${query}`);
          // TODO: Replace with actual web scraping calls
        }
        console.info("✅ Web research completed");
      }

      // AI Analysis
      if (analysisOptions.includes("Market Size & Growth")) {
        const prompt = `Analyze the market size and growth for ${companyName} in the ${industry} industry. Geographic focus: ${geographicFocus.join(", ")}`;
        results.marketSizeGrowth = await llm.generate(prompt);
      }

      if (analysisOptions.includes("Competitive Landscape")) {
        const prompt = `Analyze the competitive landscape for ${companyName} in the ${industry} industry.`;
        results.competitiveLandscape = await llm.generate(prompt);
      }

      if (analysisOptions.includes("Market Trends & Drivers")) {
        const prompt = `Analyze current and emerging trends in the ${industry} industry affecting ${companyName}.`;
        results.marketTrends = await llm.generate(prompt);
      }

      if (analysisOptions.includes("SWOT Analysis")) {
        const prompt = `Conduct a comprehensive SWOT analysis for ${companyName} in the ${industry} industry.`;
        results.swotAnalysis = await llm.generate(prompt);
      }

      if (analysisOptions.includes("Porter's Five Forces")) {
        const prompt = `Apply Porter's Five Forces framework to analyze ${companyName}'s competitive position in the ${industry} industry.`;
        results.portersFiveForces = await llm.generate(prompt);
      }

      if (analysisOptions.includes("Customer Segmentation")) {
        const prompt = `Analyze customer segmentation for ${companyName} in the ${industry} industry.`;
        results.customerSegmentation = await llm.generate(prompt);
      }

      if (analysisOptions.includes("Regulatory Environment")) {
        const prompt = `Analyze the regulatory environment for ${companyName} in the ${industry} industry.`;
        results.regulatoryEnvironment = await llm.generate(prompt);
      }

      setAnalysisResults(results);

      console.info("📝 Generating comprehensive market report...");
      const markdownReport = templateGen.generateMarketAnalysisReport(results);
      console.log(markdownReport);

      // TODO: Implement download buttons for MD & DOCX

    } catch (error) {
      console.error("Error generating analysis:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold">🌐 Market & Competitive Analysis</h1>
      <p className="text-gray-600 mb-6">AI-powered market research with web data extraction</p>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <input
          type="text"
          placeholder="Company Name e.g., Tesla"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
          className="border p-2"
        />
        <input
          type="text"
          placeholder="Industry/Sector e.g., Electric Vehicles"
          value={industry}
          onChange={(e) => setIndustry(e.target.value)}
          className="border p-2"
        />
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <select
          multiple
          value={geographicFocus}
          onChange={(e) =>
            setGeographicFocus(Array.from(e.target.selectedOptions, (o) => o.value))
          }
          className="border p-2"
        >
          {["North America", "Europe", "Asia Pacific", "Latin America", "Middle East & Africa", "Global"].map(
            (region) => (
              <option key={region} value={region}>
                {region}
              </option>
            )
          )}
        </select>

        <input
          type="text"
          placeholder="Company Website (Optional)"
          value={companyWebsite}
          onChange={(e) => setCompanyWebsite(e.target.value)}
          className="border p-2"
        />
      </div>

      <div className="mb-4">
        <label className="block mb-2 font-semibold">Analysis Scope</label>
        <select
          multiple
          value={analysisOptions}
          onChange={(e) =>
            setAnalysisOptions(Array.from(e.target.selectedOptions, (o) => o.value))
          }
          className="border p-2 w-full"
        >
          {[
            "Market Size & Growth",
            "Competitive Landscape",
            "Market Trends & Drivers",
            "SWOT Analysis",
            "Porter's Five Forces",
            "Customer Segmentation",
            "Regulatory Environment",
          ].map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </div>

      <div className="mb-6">
        <label className="inline-flex items-center">
          <input
            type="checkbox"
            checked={enableWebResearch}
            onChange={(e) => setEnableWebResearch(e.target.checked)}
            className="mr-2"
          />
          Enable Web Research
        </label>
      </div>

      <button
        onClick={generateAnalysis}
        className="bg-blue-600 text-white p-3 rounded w-full mb-6"
        disabled={loading}
      >
        {loading ? "🚀 Generating Analysis..." : "🚀 Generate Market Analysis"}
      </button>

      {analysisResults && (
        <div>
          <h2 className="text-2xl font-bold mb-2">📄 Analysis Preview</h2>
          <pre className="bg-gray-100 p-4 rounded overflow-x-auto">
            {JSON.stringify(analysisResults, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};
