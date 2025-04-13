import { describe, it, expect } from "vitest";
import capitalizeFirstLetter from "../src/utils/utils";

describe("capitalizeFirstLetter", () => {
  it("should capitalize the first letter of a lowercase word", () => {
    expect(capitalizeFirstLetter("hello")).toBe("Hello");
  });

  it("should capitalize the first letter of an uppercase word and make the rest lowercase", () => {
    expect(capitalizeFirstLetter("HELLO")).toBe("Hello");
  });

  it("should handle a mixed-case word correctly", () => {
    expect(capitalizeFirstLetter("hElLo")).toBe("Hello");
  });

  it("should return an empty string if input is an empty string", () => {
    expect(capitalizeFirstLetter("")).toBe("");
  });

  it("should handle single-character strings", () => {
    expect(capitalizeFirstLetter("a")).toBe("A");
    expect(capitalizeFirstLetter("A")).toBe("A");
  });

  it("should handle strings with spaces correctly", () => {
    expect(capitalizeFirstLetter(" hello")).toBe(" hello");
    expect(capitalizeFirstLetter("Hello world")).toBe("Hello world");
  });

  it("should handle non-alphabetic characters correctly", () => {
    expect(capitalizeFirstLetter("123abc")).toBe("123abc");
    expect(capitalizeFirstLetter("!hello")).toBe("!hello");
  });
});
