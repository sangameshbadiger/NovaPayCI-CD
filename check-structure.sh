required=(
  "README.md"
  "ERRATA.md"
  "docs/01-pipeline-architecture/architecture.md"
  "docs/02-deployment-strategies"
  "docs/03-compliance-gates"
  "docs/04-database-migration"
  "docs/05-environment-promotion"
  "docs/06-rollback-specification"
  "docs/07-runbook-playbook"
  "docs/08-observability"
  "pipeline/.github/workflows"
  "pipeline/helm"
  "pipeline/terraform"
  "pipeline/policies"
  "pipeline/scripts"
  "dashboards/grafana"
  "runbooks/deployment-runbook.md"
  "runbooks/incident-playbook.md"
  "evidence/self-assessment.md"
  "evidence/reflections.md"
  "evidence/trc-presentation.pdf"
)

missing=0
for item in "${required[@]}"; do
  if [ -e "$item" ]; then
    echo "[OK]      $item"
  else
    echo "[MISSING] $item"
    missing=$((missing + 1))
  fi
done

if [ $missing -eq 0 ]; then
  echo "=== PROJECT STRUCTURE COMPLETE ==="
else
  echo "Missing items: $missing"
  echo "PROJECT STRUCTURE INCOMPLETE"
fi
