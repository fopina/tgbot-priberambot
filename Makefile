pubdev:
	docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 \
						-t fopina/tgbot-priberambot:dev \
						--push \
						.

pub:
	docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 \
						-t fopina/tgbot-priberambot:latest \
						--push \
						.
