#!/usr/bin/env python3
"""Comprehensive Wazuh MCP Server health validation script."""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from wazuh_mcp_server.config import WazuhConfig
from wazuh_mcp_server.api.wazuh_client import WazuhAPIClient

class ServerHealthValidator:
    """Comprehensive server health validator."""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "unknown",
            "tests": {},
            "summary": {},
            "recommendations": []
        }
    
    async def run_all_tests(self):
        """Run all health validation tests."""
        print("🏥 Starting comprehensive Wazuh MCP Server health validation...")
        print("=" * 60)
        
        # Test 1: Configuration validation
        await self._test_configuration()
        
        # Test 2: Manager API connectivity
        await self._test_manager_api()
        
        # Test 3: Authentication
        await self._test_authentication()
        
        # Test 4: Core API endpoints
        await self._test_core_endpoints()
        
        # Test 5: Performance metrics
        await self._test_performance()
        
        # Generate summary and recommendations
        self._generate_summary()
        self._generate_recommendations()
        
        print("\n" + "=" * 60)
        print("🏥 Health validation completed!")
        self._print_summary()
        
        return self.results
    
    async def _test_configuration(self):
        """Test configuration loading and validation."""
        print("\n📋 Testing Configuration...")
        
        try:
            config = WazuhConfig.from_env()
            self.config = config
            
            self.results["tests"]["configuration"] = {
                "status": "pass",
                "details": {
                    "host": config.host,
                    "port": config.port,
                    "ssl_verification": config.verify_ssl,
                    "indexer_disabled": not config.use_indexer_for_alerts
                }
            }
            print(f"   ✅ Configuration loaded: {config.host}:{config.port}")
            print(f"   ✅ SSL verification: {'enabled' if config.verify_ssl else 'disabled'}")
            print(f"   ✅ Indexer features: {'disabled' if not config.use_indexer_for_alerts else 'enabled'}")
            
        except Exception as e:
            self.results["tests"]["configuration"] = {
                "status": "fail",
                "error": str(e)
            }
            print(f"   ❌ Configuration failed: {e}")
    
    async def _test_manager_api(self):
        """Test Manager API connectivity."""
        print("\n🔗 Testing Manager API Connectivity...")
        
        try:
            self.client = WazuhAPIClient(self.config)
            await self.client.__aenter__()
            
            self.results["tests"]["manager_connectivity"] = {
                "status": "pass",
                "details": {
                    "base_url": self.config.base_url,
                    "protocol": "https"
                }
            }
            print(f"   ✅ Connected to {self.config.base_url}")
            
        except Exception as e:
            self.results["tests"]["manager_connectivity"] = {
                "status": "fail",
                "error": str(e)
            }
            print(f"   ❌ Connection failed: {e}")
    
    async def _test_authentication(self):
        """Test authentication with Wazuh Manager."""
        print("\n🔐 Testing Authentication...")
        
        try:
            await self.client.authenticate()
            
            self.results["tests"]["authentication"] = {
                "status": "pass",
                "details": {
                    "username": self.config.username,
                    "token_valid": True
                }
            }
            print(f"   ✅ Authentication successful for user: {self.config.username}")
            
        except Exception as e:
            self.results["tests"]["authentication"] = {
                "status": "fail",
                "error": str(e)
            }
            print(f"   ❌ Authentication failed: {e}")
    
    async def _test_core_endpoints(self):
        """Test core API endpoints."""
        print("\n🎯 Testing Core API Endpoints...")
        
        endpoints = {
            "api_info": ("/", "API information"),
            "agents": ("/agents", "Agent management"),
            "alerts": ("alerts", "Security alerts"),
            "rules": ("/rules", "Detection rules")
        }
        
        endpoint_results = {}
        
        for endpoint_name, (path, description) in endpoints.items():
            try:
                if endpoint_name == "api_info":
                    # API info endpoint doesn't accept limit parameter
                    result = await self.client._request("GET", path)
                elif endpoint_name == "alerts":
                    # Use the client method for alerts
                    result = await self.client.get_alerts(limit=1)
                else:
                    # Other endpoints with limit parameter
                    result = await self.client._request("GET", path + "?limit=1")
                
                if result and (result.get('data') or result.get('error') == 0):
                    endpoint_results[endpoint_name] = {
                        "status": "pass",
                        "description": description,
                        "response_size": len(str(result))
                    }
                    print(f"   ✅ {description}: Working")
                else:
                    endpoint_results[endpoint_name] = {
                        "status": "warn",
                        "description": description,
                        "message": "No data returned"
                    }
                    print(f"   ⚠️  {description}: No data")
                    
            except Exception as e:
                endpoint_results[endpoint_name] = {
                    "status": "fail",
                    "description": description,
                    "error": str(e)
                }
                print(f"   ❌ {description}: {e}")
        
        self.results["tests"]["core_endpoints"] = endpoint_results
    
    async def _test_performance(self):
        """Test basic performance metrics."""
        print("\n⚡ Testing Performance...")
        
        try:
            import time
            start_time = time.time()
            
            # Test a simple API call
            await self.client._request("GET", "/")
            
            response_time = time.time() - start_time
            
            self.results["tests"]["performance"] = {
                "status": "pass",
                "details": {
                    "api_response_time_ms": round(response_time * 1000, 2),
                    "performance_rating": "good" if response_time < 2.0 else "slow"
                }
            }
            
            rating = "good" if response_time < 2.0 else "slow"
            print(f"   ✅ API response time: {response_time:.2f}s ({rating})")
            
        except Exception as e:
            self.results["tests"]["performance"] = {
                "status": "fail",
                "error": str(e)
            }
            print(f"   ❌ Performance test failed: {e}")
    
    def _generate_summary(self):
        """Generate test summary."""
        total_tests = len(self.results["tests"])
        passed_tests = sum(1 for test in self.results["tests"].values() if test.get("status") == "pass")
        failed_tests = sum(1 for test in self.results["tests"].values() if test.get("status") == "fail")
        warned_tests = sum(1 for test in self.results["tests"].values() if test.get("status") == "warn")
        
        if failed_tests == 0 and warned_tests == 0:
            overall_status = "healthy"
        elif failed_tests == 0:
            overall_status = "warning"
        else:
            overall_status = "unhealthy"
        
        self.results["overall_status"] = overall_status
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "warnings": warned_tests,
            "success_rate": round((passed_tests / total_tests) * 100, 1) if total_tests > 0 else 0
        }
    
    def _generate_recommendations(self):
        """Generate recommendations based on test results."""
        recommendations = []
        
        # Check SSL configuration
        if not self.config.verify_ssl:
            recommendations.append("Consider enabling SSL verification for production use")
        
        # Check authentication
        if self.config.username.lower() in ["admin", "wazuh", "user"]:
            recommendations.append("Use a custom username instead of default credentials")
        
        # Check performance
        perf_test = self.results["tests"].get("performance", {})
        if perf_test.get("details", {}).get("performance_rating") == "slow":
            recommendations.append("API response time is slow - check network connectivity")
        
        # Check failed tests
        failed_tests = [name for name, test in self.results["tests"].items() if test.get("status") == "fail"]
        if failed_tests:
            recommendations.append(f"Fix failed tests: {', '.join(failed_tests)}")
        
        if not recommendations:
            recommendations.append("Server is healthy - no immediate actions required")
        
        self.results["recommendations"] = recommendations
    
    def _print_summary(self):
        """Print formatted summary."""
        summary = self.results["summary"]
        status = self.results["overall_status"]
        
        status_icon = {
            "healthy": "🟢",
            "warning": "🟡", 
            "unhealthy": "🔴"
        }.get(status, "⚪")
        
        print(f"\n{status_icon} OVERALL STATUS: {status.upper()}")
        print(f"📊 Test Results: {summary['passed']}/{summary['total_tests']} passed ({summary['success_rate']}%)")
        
        if summary['failed'] > 0:
            print(f"❌ Failed: {summary['failed']}")
        if summary['warnings'] > 0:
            print(f"⚠️  Warnings: {summary['warnings']}")
        
        print("\n💡 RECOMMENDATIONS:")
        for rec in self.results["recommendations"]:
            print(f"   • {rec}")
    
    async def cleanup(self):
        """Cleanup resources."""
        if hasattr(self, 'client'):
            await self.client.__aexit__(None, None, None)

async def main():
    """Main validation function."""
    validator = ServerHealthValidator()
    
    try:
        results = await validator.run_all_tests()
        
        # Save results to file
        with open("server_health_report.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: server_health_report.json")
        
        # Exit with appropriate code
        return 0 if results["overall_status"] in ["healthy", "warning"] else 1
        
    except Exception as e:
        print(f"\n❌ Validation failed with error: {e}")
        return 1
    
    finally:
        await validator.cleanup()

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)