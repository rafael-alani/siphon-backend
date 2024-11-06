const { randomUUID } = require("crypto");

// Demo Companies
const companies = [
  {
    name: "EcoGrid Solutions",
    location: "Amsterdam",
    statuses: [
      {
        commodity: "Electricity",
        status: "surplus",
        amount: { value: 500, measurement_unit: "MWh" },
      },
      {
        commodity: "Heat",
        status: "deficit",
        amount: { value: 200, measurement_unit: "GJ" },
      },
    ],
  },
  {
    name: "GreenHydro Corp",
    location: "Berlin",
    statuses: [
      {
        commodity: "Hydrogen",
        status: "surplus",
        amount: { value: 300, measurement_unit: "kg" },
      },
      {
        commodity: "Electricity",
        status: "deficit",
        amount: { value: 400, measurement_unit: "MWh" },
      },
    ],
  },
  {
    name: "SolarTech Industries",
    location: "Barcelona",
    statuses: [
      {
        commodity: "Electricity",
        status: "surplus",
        amount: { value: 800, measurement_unit: "MWh" },
      },
      {
        commodity: "Gas",
        status: "deficit",
        amount: { value: 150, measurement_unit: "MMBtu" },
      },
    ],
  },
  {
    name: "WindPower Dynamics",
    location: "Copenhagen",
    statuses: [
      {
        commodity: "Electricity",
        status: "surplus",
        amount: { value: 600, measurement_unit: "MWh" },
      },
      {
        commodity: "Heat",
        status: "surplus",
        amount: { value: 250, measurement_unit: "GJ" },
      },
    ],
  },
  {
    name: "ThermalEnergy Plus",
    location: "Vienna",
    statuses: [
      {
        commodity: "Heat",
        status: "surplus",
        amount: { value: 450, measurement_unit: "GJ" },
      },
      {
        commodity: "Gas",
        status: "surplus",
        amount: { value: 200, measurement_unit: "MMBtu" },
      },
    ],
  },
  {
    name: "HydrogenTech Solutions",
    location: "Stockholm",
    statuses: [
      {
        commodity: "Hydrogen",
        status: "surplus",
        amount: { value: 500, measurement_unit: "kg" },
      },
      {
        commodity: "Electricity",
        status: "deficit",
        amount: { value: 300, measurement_unit: "MWh" },
      },
    ],
  },
];

// Commodity configurations
const commodityConfigs = {
  Electricity: {
    basePrice: 80,
    unit: "MWh",
    volatility: 0.25,
    seasonalImpact: 0.2,
    trendFactor: 11.2,
  },
  Hydrogen: {
    basePrice: 10,
    unit: "kg",
    volatility: 0.35,
    seasonalImpact: 0.1,
    trendFactor: 11.5,
  },
  Heat: {
    basePrice: 30,
    unit: "GJ",
    volatility: 0.2,
    seasonalImpact: 0.3,
    trendFactor: 11.0,
  },
  Gas: {
    basePrice: 20,
    unit: "MMBtu",
    volatility: 0.3,
    seasonalImpact: 0.25,
    trendFactor: 11.3,
  },
};

// Generate random price with seasonal variation
function generatePrice(commodity, date) {
  const config = commodityConfigs[commodity];

  // Calculate days since start of the year for trend
  const startOfYear = new Date(date.getFullYear(), 0, 1);
  const daysSinceStart = (date - startOfYear) / (1000 * 60 * 60 * 24);

  // Enhanced trend calculation - more pronounced upward trend
  const yearProgress = daysSinceStart / 365;
  const trendImpact = yearProgress * 100 * config.trendFactor;

  // Seasonal variation (sine wave throughout the year)
  const seasonalFactor =
    Math.sin(((date.getMonth() + 1) * Math.PI) / 6) * config.seasonalImpact;

  // Random volatility
  const randomFactor = (Math.random() - 0.5) * 2 * config.volatility;

  // Base price increases with trend
  const trendedBasePrice = config.basePrice * (1 + trendImpact);

  // Apply seasonal and random factors to trended base price
  // let price = trendedBasePrice * (1 + seasonalFactor + randomFactor);
  let price = trendedBasePrice;

  // Add occasional price spikes (5% chance)
  if (Math.random() < 0.05) {
    price *= 1 + Math.random() * 0.5; // Up to 50% spike
  }

  return price;
}

// Generate random amount for a commodity
function generateAmount(commodity) {
  const config = commodityConfigs[commodity];
  const baseAmount = Math.floor(Math.random() * 100) + 50;
  return {
    value: baseAmount,
    measurement_unit: config.unit,
  };
}

// Generate trades for the past year with varying density
function generateHistoricalTrades() {
  const trades = [];
  const endDate = new Date();
  const startDate = new Date(endDate);
  startDate.setFullYear(startDate.getFullYear() - 1);

  // Helper function to add a trade
  const addTrade = (date) => {
    const commodity =
      Object.keys(commodityConfigs)[
        Math.floor(Math.random() * Object.keys(commodityConfigs).length)
      ];
    const requesterIdx = Math.floor(Math.random() * companies.length);
    let fulfillerIdx;
    do {
      fulfillerIdx = Math.floor(Math.random() * companies.length);
    } while (fulfillerIdx === requesterIdx);

    const price = generatePrice(commodity, date);
    const amount = generateAmount(commodity);

    trades.push({
      id: randomUUID(),
      commodity,
      type: Math.random() < 0.5 ? "buy" : "sell",
      amount,
      price: {
        value: price,
        currency: "EUR",
      },
      status: "Completed",
      time: new Date(date),
      requester_company: companies[requesterIdx].name,
      fulfiller_company: companies[fulfillerIdx].name,
    });
  };

  // Generate trades with different densities based on time periods
  const now = endDate.getTime();
  const last24h = now - 24 * 60 * 60 * 1000;
  const last7d = now - 7 * 24 * 60 * 60 * 1000;
  const last30d = now - 30 * 24 * 60 * 60 * 1000;
  const lastYear = startDate.getTime();

  // Last 24 hours: ~48 trades (every 30 minutes)
  for (let t = last24h; t <= now; t += 30 * 60 * 1000) {
    addTrade(new Date(t));
  }

  // Last 7 days (excluding last 24h): ~84 trades (every 2 hours)
  for (let t = last7d; t < last24h; t += 2 * 60 * 60 * 1000) {
    addTrade(new Date(t));
  }

  // Last 30 days (excluding last 7d): ~92 trades (every 6 hours)
  for (let t = last30d; t < last7d; t += 6 * 60 * 60 * 1000) {
    addTrade(new Date(t));
  }

  // Rest of the year: ~276 trades (every 24 hours)
  for (let t = lastYear; t < last30d; t += 24 * 60 * 60 * 1000) {
    addTrade(new Date(t));
  }

  return trades;
}

// Generate the data
const historicalTrades = generateHistoricalTrades();

// Write to files
const fs = require("fs");

// Save companies
fs.writeFileSync("demo_companies.json", JSON.stringify(companies, null, 2));

// Save historical trades
fs.writeFileSync("demo_trades.json", JSON.stringify(historicalTrades, null, 2));

console.log(`Generated ${companies.length} companies`);
console.log(`Generated ${historicalTrades.length} historical trades`);
