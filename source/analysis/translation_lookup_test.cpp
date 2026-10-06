#include "../translation_lookup.h"

#include <cstdio>

int main() {
    MariTranslation::Lookup lookup;
    auto check = [&](const char *caseName, const QString &source,
                     const QString &expected) {
        if (lookup.find(source) == expected) return true;
        std::fprintf(stderr, "FAIL: %s\n", caseName);
        return false;
    };

    if (!check("missing dictionary", QStringLiteral("File"), {})) return 1;
    lookup.add(QStringLiteral("File"), QStringLiteral("文件"));
    lookup.add(QStringLiteral("Rough Glass"), QStringLiteral("粗糙玻璃"));
    lookup.add(QStringLiteral("Sand"), QStringLiteral("沙"));
    lookup.add(QStringLiteral("sand"), QStringLiteral("砂"));
    lookup.rebuild();

    if (!check("exact", QStringLiteral("File"), QStringLiteral("文件")) ||
        !check("mnemonic and state", QStringLiteral("&File*"), QStringLiteral("文件*")) ||
        !check("case and underscore", QStringLiteral("ROUGH_GLASS"), QStringLiteral("粗糙玻璃")) ||
        !check("fullwidth underscore", QStringLiteral("Ｒｏｕｇｈ＿Ｇｌａｓｓ"), QStringLiteral("粗糙玻璃")) ||
        !check("elided", QStringLiteral("&Rough..."), QStringLiteral("粗糙玻璃")) ||
        !check("exact conflict A", QStringLiteral("Sand"), QStringLiteral("沙")) ||
        !check("exact conflict B", QStringLiteral("sand"), QStringLiteral("砂")) ||
        !check("ambiguous fallback", QStringLiteral("SAND"), {})) return 1;

    std::puts("PASS: exact, mnemonic, normalized, elided and ambiguous lookups");
    return 0;
}
