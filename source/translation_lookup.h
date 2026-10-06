#pragma once

#include <QtCore/QHash>
#include <QtCore/QPair>
#include <QtCore/QString>

#include <vector>

// Exact dictionary entries remain authoritative. Normalized and elided
// matching are display-only fallbacks and never rewrite the source model.
namespace MariTranslation {

class Lookup final {
public:
    void add(const QString &source, const QString &translated);
    void rebuild();
    QString find(const QString &text) const;

private:
    QString findElided(const QString &text) const;

    QHash<QString, QString> exact_;
    QHash<QString, QString> normalized_;
    std::vector<QPair<QString, QString>> sortedKeys_;
};

} // namespace MariTranslation
