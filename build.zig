const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // === shared C library: (gcc -lm -shared -fPIC -o bin/c_ldpc.dll src/c_ldpc.c)
    const cLdpc = b.addSharedLibrary(.{
        .name = "c_ldpc",
        .root_source_file = null, // pure-C module, no Zig entry point
        .target = target,
        .optimize = optimize,
    });
    // wrap your .c file in a Module.CSourceFile literal:
    cLdpc.addCSourceFile(.{
        .file = b.path("gf3/src/c_ldpc.c"),
        .flags = &[_][]const u8{}, // no extra flags here
    }); // :contentReference[oaicite:0]{index=0}
    cLdpc.linkSystemLibrary("m");
    b.installArtifact(cLdpc);

    // === executable: (gcc -o bin/results2csv src/results2csv.c)
    const results2csv = b.addExecutable(.{
        .name = "results2csv",
        .root_source_file = null,
        .target = target,
        .optimize = optimize,
    });
    results2csv.addCSourceFile(.{
        .file = b.path("gf3/src/results2csv.c"),
        .flags = &[_][]const u8{},
    }); // :contentReference[oaicite:1]{index=1}
    results2csv.linkLibC();
    b.installArtifact(results2csv);
}
