import React, { useEffect, useState } from 'react';
import { DollarSign, ShoppingBag, Users, TrendingUp, RefreshCw } from 'lucide-react';
import MetricCard from './MetricCard';
import SalesTrendChart from './SalesTrendChart';
import CategoryChart from './CategoryChart';
import RegionalChart from './RegionalChart';
import TopProductsTable from './TopProductsTable';
import {
  fetchDashboardOverview,
  fetchMonthlyTrend,
  fetchCategoryPerformance,
  fetchRegionalPerformance,
  fetchTopProducts
} from '../../services/api';

export default function DashboardView() {
  const [overview, setOverview] = useState(null);
  const [monthlyTrend, setMonthlyTrend] = useState([]);
  const [categories, setCategories] = useState([]);
  const [regional, setRegional] = useState([]);
  const [topProducts, setTopProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    try {
      const [ov, mt, cat, reg, topP] = await Promise.all([
        fetchDashboardOverview(),
        fetchMonthlyTrend(),
        fetchCategoryPerformance(),
        fetchRegionalPerformance(),
        fetchTopProducts()
      ]);
      setOverview(ov);
      setMonthlyTrend(mt);
      setCategories(cat);
      setRegional(reg);
      setTopProducts(topP);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex items-center space-x-3 text-indigo-400 font-medium">
          <RefreshCw className="w-6 h-6 animate-spin" />
          <span>Loading Sales Intelligence Engine...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white font-outfit">Sales Executive Dashboard</h1>
          <p className="text-slate-400 text-sm mt-1">Real-time revenue performance, order metrics, and product insights</p>
        </div>
        <button
          onClick={loadData}
          className="self-start sm:self-auto flex items-center space-x-2 px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 transition-all text-sm font-medium"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Refresh Data</span>
        </button>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total Revenue"
          value={overview ? `$${overview.total_revenue.toLocaleString()}` : '$0'}
          subtitle="Lifetime completed gross sales"
          change={overview?.monthly_growth_percent}
          icon={DollarSign}
          color="indigo"
        />
        <MetricCard
          title="Total Orders"
          value={overview ? overview.total_orders.toLocaleString() : '0'}
          subtitle="Processed completed orders"
          icon={ShoppingBag}
          color="emerald"
        />
        <MetricCard
          title="Avg Order Value (AOV)"
          value={overview ? `$${overview.avg_order_value.toLocaleString()}` : '$0'}
          subtitle="Mean revenue per transaction"
          icon={TrendingUp}
          color="amber"
        />
        <MetricCard
          title="Active Customers"
          value={overview ? overview.active_customers.toLocaleString() : '0'}
          subtitle="Unique purchasing accounts"
          icon={Users}
          color="violet"
        />
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <SalesTrendChart data={monthlyTrend} />
        </div>
        <div>
          <CategoryChart data={categories} />
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RegionalChart data={regional} />
        <TopProductsTable products={topProducts} />
      </div>

    </div>
  );
}
