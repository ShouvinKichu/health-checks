#!/bin/bash


COUNT=$(grep -c ERROR health.log)
echo "total error: $COUNT"