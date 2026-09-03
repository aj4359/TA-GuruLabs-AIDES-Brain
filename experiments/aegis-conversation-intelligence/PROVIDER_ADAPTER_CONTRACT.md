# AEGIS Streaming Speech Provider Contract

## Purpose

Allow AEGIS to test speaker-aware streaming transcription without coupling the product to a single speech vendor or weakening the consent/privacy boundary.

## Required provider capabilities

A provider adapter may expose:
- streaming or chunked transcription
- speaker-labelled segments when available
- segment timing
- final/partial segment state

## Required AEGIS controls

Before any provider receives audio:
1. Every participant must explicitly consent to capture.
2. Capture/transcription state must be visible in the eventual product UI.
3. The session must have an immediate stop path.
4. Raw audio and full transcript remain ephemeral by default.
5. Retention decisions remain outside the provider adapter.

## Provider-neutral rule

`StreamingSpeechProvider` is the only interface the experiment depends on. A future VibeVoice, cloud speech, on-device, or other compliant adapter can implement it without changing session policy.

## Data boundary

Provider adapters must not:
- write directly to general AIDES memory
- decide retention
- infer deception, mental health, compatibility, toxicity, or relationship quality
- silently expand the list of participants or consent scope

## Security boundary

No provider secrets, API tokens, private endpoints, customer identifiers, or real intimate recordings belong in this public repository.

## Current status

The repository contains only the interface and a fake test provider. No live speech service is integrated yet.
