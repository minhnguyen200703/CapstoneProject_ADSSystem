import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Overview from './pages/overview/Overview';
import Plan from './pages/plan/Plan';
import Layout from './Layout'; // Import the Layout component

export default function App() {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <Layout>
              <Overview />
            </Layout>
          }
        />
        <Route
          path="/plan"
          element={
            <Layout>
              <Plan />
            </Layout>
          }
        />
      </Routes>
    </Router>
  );
}