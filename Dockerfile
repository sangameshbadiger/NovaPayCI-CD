FROM gcr.io/distroless/static-debian12:nonroot

WORKDIR /app

# Copy application binary/artifacts directly from host repository context
COPY . /app/

USER nonroot:nonroot

ENTRYPOINT ["/app/novapay-app"]
